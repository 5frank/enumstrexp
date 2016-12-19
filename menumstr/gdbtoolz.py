import gdb
import logging
import re
log = logging.getLogger(__file__)

def loadSymbols(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    assert(not r) #, 'gdb.execute returned %s', str(r))

def getDefSource(symbName):
    """ source file and path where enum is defined.
       Fails if symbName is enum member."""
    r = gdb.execute('info types ^'+symbName +'$', False, True)
    for l in r.splitlines():
        if l.startswith('File'):
            return l.strip().lstrip('File').rstrip(':')
    return None

def getEnumDict(enumId, scope=None):
    t = None
    def isEnum(t):
        if t == None: return False
        ts = t.strip_typedefs()
        if ts.code == gdb.TYPE_CODE_ENUM: return True
        return False
    # Type from enum typedef id
    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(enumId))
        if not isEnum(t):
            return None
    except RuntimeError:
        # Try find type from enum member name
        try:
            t = gdb.parse_and_eval(enumId).type
            if not isEnum(t):
                return None
        except RuntimeError:
            return None
    # success, enum instance found
    bt = gdb.types.get_basic_type(t)
    enumDict =  gdb.types.make_enum_dict(bt)
    return enumDict


def getFuncIOTypes(func, srcfile=''):
    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(func))
    except RuntimeError:
        # Try find type from enum member name
        try:
            t = gdb.parse_and_eval(func).type
            t = gdb.types.get_basic_type(t)
        except RuntimeError:
            return None, None
    s = str(t)
    m = re.search(r'(.*?)\((.*?)\)', s)
    rettype = m.group(1)
    prmtype = m.group(2) # will give all params if more then one
    return rettype, prmtype
    #return m #str(m.group(0))

def getStrArray(instance):
    ary = []
    for i in xrange(0,7): # in instance: #.type.fields(): FIXME
        v = instance[i]
        v = str(v.string())
        if v.endswith('""'):
            v = v.rstrip('""') # FIXME why ""?
        if v:
            ary.append(v)
    return ary

def getStructAsDict(addr, structtype, scope=''):
    try:
        jobtype = gdb.lookup_type(structtype)
        jobaddr = gdb.Value(long(addr, 16))
        jobptr = jobaddr.cast(jobtype.pointer())
        jobinstance = jobptr.dereference()

        job = {}
        for field in jobinstance.type.fields():
            fname = field.name
            ftype = field.type
            fval = jobinstance[fname]
            c = fval.type.code
            if c == gdb.TYPE_CODE_PTR:
                v = str(fval.string())#.dereference()
                #v = v.fetch_lazy()
                #v = v.string()
                if v.startswith('"') and v.endswith('"'):
                    v = v.strip('"')
            elif c == gdb.TYPE_CODE_INT:
                v = int(fval)
            elif c == gdb.TYPE_CODE_STRUCT or c == gdb.TYPE_CODE_UNION:
                log.error('Not handled WTF!')
            elif c == gdb.TYPE_CODE_ARRAY:
                v = getStrArray(fval)
            else:
                log.warning('Not x handled WTF!')
                v = str(fval)

            #log.debug('k:"{}", t:"{}",  v:"{}"'.format(fname, ftype, v))
            #print(fval) #print(dir(fval))
            job[str(fname)] = v
        #for name, field in jobstruct.type.iteritems():
        log.debug(job)

        return job

    except gdb.error as e:
        log.error(str(e))
    except RuntimeError as e:
        log.error(str(e))
    return None
