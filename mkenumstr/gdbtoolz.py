import gdb
import logging
import os
import sys
import re
log = logging.getLogger(os.path.basename(__file__))


class EmumInfo(object):
    def __init__(self, members={}, defsrc='', name=''):
        self.members = members
        self.defsrc = defsrc
        self.name = name

class FuncInfo(object):
    def __init__(self, rettype=None, prmtype=None):
        self.rettype = rettype
        self.prmtype = prmtype
        self.prmszie = None

def byteify(x):
    ''' python < 3. convert unicode to string '''
    if sys.version_info[0] >= 3:
        return x
    if isinstance(x, dict):
        return {byteify(key): byteify(value)
                for key, value in x.iteritems()}
    elif isinstance(x, list):
        return [byteify(element) for element in x]
    elif isinstance(x, unicode):
        return x.encode('utf-8')
    else:
        return x

def isCStr(s):
    return s.startswith('"') and s.endswith('"')

def stripCStr(s):
    return s[1:-1] if isCStr(s) else s

def loadSymbols(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    assert(not r) #, 'gdb.execute returned %s', str(r))

def isEnumType(t):
    if t is None:
        return False
    ts = t.strip_typedefs()
    if ts.code == gdb.TYPE_CODE_ENUM:
        return True
    return False

def getStructDict(addr, structtype, scope=''):
    try:
        jobtype = gdb.lookup_type(structtype)
        jobaddr = gdb.Value(long(addr, 16))
        jobptr = jobaddr.cast(jobtype.pointer())
        jobinstance = jobptr.dereference()

        job = {}
        for field in jobinstance.type.fields():
            fname = field.name
            #log.debug(fname)
            ftype = field.type
            fval = jobinstance[fname]
            c = fval.type.code
            if c == gdb.TYPE_CODE_PTR:
                if fval:
                    v = str(fval.string())
                    v = stripCStr(v) #why?
                else:
                    v = None
            elif c == gdb.TYPE_CODE_INT:
                v = int(fval)
            elif c == gdb.TYPE_CODE_STRUCT or c == gdb.TYPE_CODE_UNION:
                log.error('Not handled WTF!')
            elif c == gdb.TYPE_CODE_ARRAY:
                pass#v = gdb_getStrAry(fval)
            else:
                log.warning('Not x handled WTF!')
                v = str(fval)

            #log.debug('k:"{}", t:"{}",  v:"{}"'.format(fname, ftype, v))
            #print(fval) #print(dir(fval))
            job[str(fname)] = v

        return job

    except gdb.error as e:
        log.error(str(e))
    except RuntimeError as e:
        log.error(str(e))
    return None


def getBasicType(enumTypeName):
    try:
        t = gdb.lookup_type(enumTypeName)
        return gdb.types.get_basic_type(t)
    except RuntimeError:
        pass
    # Try find type from enum member name
    try:
        t = gdb.parse_and_eval(enumTypeName).type
        return gdb.types.get_basic_type(t)
    except RuntimeError:
        pass

    return None

def getDefSource(symbName):
    """ source file and path where enum is defined.
       Fails if symbName is enum member."""
    r = gdb.execute('info types ^'+symbName +'$', False, True)
    for l in r.splitlines():
        if l.startswith('File'):
            return l.strip().lstrip('File').rstrip(':')
    return None


def getFuncInfo(funcname, srcfile=''):
    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(funcname))
    except RuntimeError:
        try:
            t = gdb.parse_and_eval(funcname).type
            t = gdb.types.get_basic_type(t)
        except RuntimeError:
            return None

    s = str(t)
    m = re.search(r'(.*?)\((.*?)\)', s)
    fnfo = FuncInfo()
    fnfo.rettype = m.group(1)
    fnfo.prmtype = m.group(2) # will give all params if more then one
    return fnfo
    #return m #str(m.group(0))

def _mergeEnumDefs(enumdefs, unique=True):
    members = {}
    defsrcs = []
    names = []
    for ed in enumdefs:
        # TODO check conficts
        members.update(ed.members)
        defsrcs.append(ed.defsrc)
        names.append(ed.name)

    return EmumInfo(members, ','.join(defsrcs), ','.join(names))

def lookupEnums(findexpr, mergedefs=False):
    # first tryexact
    btype = getBasicType(findexpr)
    if btype is not None and isEnumType(btype):
        log.debug('Found exact type "%s"', findexpr)
        members = gdb.types.make_enum_dict(btype)
        defsrc = getDefSource(findexpr)
        name = btype.tag if btype.tag is not None else btype.name
        return [EmumInfo(members, defsrc, name)]
        #return enumdefs, defsrcfile
    enumsfound = {}

    rmpre = 'enum '
    if findexpr.startswith(rmpre):
        findexpr = findexpr[len(rmpre):]
    log.debug('findexpr "%s"', findexpr)

    r = gdb.execute('info types {}'.format(findexpr), False, True)
    #suspects
    for line in r.splitlines():
        log.debug('  %s', line)
        if line.startswith('File'):
            defsrc =  line.strip().lstrip('File').rstrip(':')
            continue

        x = line.rstrip(';').split()
        if 'enum' not in x:
            continue

        i = x.index('enum')
        if len(x) < (i+1):
            log.debug('  ignoring line "{}"'.format(line))
            continue
        candidate = x[i] + ' ' + x[i+1]

        log.debug('Looking up candidate:%s', candidate)
        btype = getBasicType(candidate)
        log.debug('Basic type tag:%s, name: %s', btype.tag, btype.name)
        if not isEnumType(btype):
            continue

        name = btype.tag if btype.tag is not None else btype.name
        assert(name)
        if name in enumsfound:
            log.debug('duplicate defs of "%s"', str(name))
            continue # TODO compare dups?
        members = gdb.types.make_enum_dict(btype)

        enumsfound[name] = EmumInfo(members, defsrc, name)

    return enumsfound.values()
