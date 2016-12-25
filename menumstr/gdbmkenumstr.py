import gdb
import os
import logging
import re
import subprocess
from pprint import pprint

#needed as python invoked by gdb
scriptDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scriptDir) #
import envarg

log = logging.getLogger(os.path.basename(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)

def isCStr(s):
    return s.startswith('"') and s.endswith('"')

def stripCStr(s):
    return s[1:-1] if isCStr(s) else s

def fullrelpath(p):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisdir, p)

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

def gdb_loadSymbols(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    assert(not r) #, 'gdb.execute returned %s', str(r))

def gdb_isEnumType(t):
    if t == None: return False
    ts = t.strip_typedefs()
    if ts.code == gdb.TYPE_CODE_ENUM: return True
    return False


def gdb_getStructDict(addr, structtype, scope=''):
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
        #for name, field in jobstruct.type.iteritems():

        return job

    except gdb.error as e:
        log.error(str(e))
    except RuntimeError as e:
        log.error(str(e))
    return None


def nm_findInstances(symbfile, prefix):
    '''
    gdb unable to retrive these, diffrent symbol table!?
    like $ nm -C main.o | grep $PREFIX | cut -d ' ' -f 1
    but a little bit more secure. sigh
    '''
    assert(os.path.exists(symbfile))
    addrs = []

    cmd = ['nm', '-C', symbfile]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None
    for line in out.split('\n'):
        if not line:
            continue
        cols = line.split(' ')
        if len(cols) < 3:
            log.debug('Ignoring nm line:%s', line)
            continue
        addr = cols[0]
        styp = cols[1]
        symb = cols[2]
        if not symb.startswith(prefix):
            continue

        if styp != 'd': #"d" The symbol is in the initialized data section.
            log.warning('Symbol %s at %s of type ("%s")', symb, addr, styp)

        addrs.append(addr)

    return addrs

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


def findenums(findexpr, mergedefs=False):
    # first tryexact
    btype = getBasicType(findexpr)
    if btype is not None and gdb_isEnumType(btype):
        log.debug('Found exact type "%s"', findexpr)
        defsrcfile = getDefSource(findexpr)
        enumdefs = gdb.types.make_enum_dict(btype)
        return enumdefs, defsrcfile

    enumsfound = {}

    rmpre = 'enum '
    if findexpr.startswith(rmpre):
        findexpr = findexpr[len(rmpre):]
    log.debug('findexpr "%s"', findexpr)

    r = gdb.execute('info types {}'.format(findexpr), False, True)
    #suspects
    for line in r.splitlines():
        log.debug('XX: %s', line)
        if line.startswith('File'):
            defsrcfile =  line.strip().lstrip('File').rstrip(':')
            continue

        x = line.rstrip(';').split()
        if 'enum' not in x:
            continue

        i = x.index('enum')
        if len(x) < (i+1):
            print('ignoring line "{}"'.format(line))
            continue
        candidate = x[i] + ' ' + x[i+1]

        log.debug('Looking up candidate:%s', candidate)
        btype = getBasicType(candidate)
        log.debug('Basic type tag:%s, name: %s', btype.tag, btype.name)
        if not gdb_isEnumType(btype):
            continue

        btypename = btype.tag if btype.tag is not None else btype.name
        assert(btypename)
        if btypename in enumsfound:
            log.debug('duplicate defs of "%s"', btypename)
            continue # TODO compare dups?
        enumdefs = gdb.types.make_enum_dict(btype)
        enumsfound[btypename] = (enumdefs, defsrcfile)

    if len(enumsfound) == 0:
        raise LookupError
    elif len(enumsfound) == 1:
        k, (enumdefs, defsrcfile) = enumsfound.popitem()
        return enumdefs, defsrcfile
    elif mergedefs:
        defsrcfiles = []
        enumdefs = {}
        for _enumdefs, _defsrcfile in enumsfound.items():
            # TODO check conficts
            defsrcfiles.append(_defsrcfile)
            enumdefs.update(_enumdefs)

        return enumdefs, ','.join(defsrcfiles)
    else:
        raise LookupError


def makeEnumRepr(job, joindupsep='=='):
    strstrip  = job['args']['strstrip']
    exclude   = job['args']['exclude']
    emnumdefs = job['enumdefs']

    log.debug(emnumdefs)

    if strstrip is not None:
        restrip = re.compile(strstrip)
        stripper = lambda x : restrip.sub('', x)
    else:
        stripper = lambda x : x

    if exclude:
        reexcl = re.compile(exclude)
        excluder = lambda x : reexcl.search(x) is not None
    else:
        excluder = lambda x : False

    excluded = {}
    enumrepr = {}
    for name, val in emnumdefs.items():
        if excluder(name):
            strname = None
        else:
            strname = stripper(name)

        enumrepr[name] = strname
    return enumrepr


def genFuncParamName(job):
    usebitpos   = job['args']['usebitpos']
    return 'bitpos' if usebitpos else 'value'

def genFuncProto(job, prmname, withcomments=True, term=''):
    funcname    = job['args']['funcname']
    funcprmtype = job['args']['funcprmtype']
    usebitpos   = job['args']['usebitpos']
    prmname = genFuncParamName(job)

    src = []
    if usebitpos:
        brief = 'Enum bit flag index to string lookup'
        param = 'bit position index representing a enum flag. (LSB == 0)'
    else:

        brief = 'Enum value to string lookup.'
        param = 'enum value.'

    if withcomments:
        src.extend([
            '/**',
            ' * @brief {}'.format(brief),
            ' * @note  Do not modify! Auto generated code.',
            ' * @param {} - {}\n'.format(prmname, param)
        ])
        #for k, v in job.propsrc.items():
        #    if v: src.append(' *    {}: {}'.format(k, v)) #FIXME escape c '*/' etc
        src.append(' */')

    prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                        func=funcname,
                        prmtype=funcprmtype,
                        prmname=prmname,
                        term=term)

    src.append(prototype)

    return src


def genFuncSrc(job):
    enumdefs    = job['enumdefs']
    enumrepr    = job['enumrepr']
    usebitpos   = job['args']['usebitpos']
    usedefs     = True,
    nameunknown = '??'
    tabstyle    = '  '
    xindent = ''
    prmname = genFuncParamName(job)

    src = genFuncProto(job, prmname, term='\n{')

    tabs = lambda n : n * tabstyle
    src.extend([
        '{}switch({})'.format(tabs(1), prmname),
        '{}{{'.format(tabs(1))# escpae '{' with '{{'
    ])

    excluded = []
    for defname in sorted(enumdefs, key=enumdefs.get): # sor by value
        strname = enumrepr[defname]
        if strname is None:
            excluded.append(defname)
            continue
        caselbl = defname if usedefs else int(enumdefs[defname])
        if usebitpos: caselbl = 'BITPOS32({})'.format(caselbl)

        src.extend([
            '{}case {}:'.format(tabs(2), caselbl),
            '{}return {}"{}";'.format(tabs(3), xindent, strname)
        ])

    for defname in excluded:
        caselbl = defname if usedefs else int(enumdefs[defname])
        src.extend([
            '{}case {}: /* excluded */'.format(tabs(2), caselbl)
        ])

    src.extend([
        '{}default:'.format(tabs(2)),
        '{}return "{}";'.format(tabs(2), nameunknown),
        '{}}}'.format(tabs(1)) # escpae '}' with '}}'
    ])
    # ---- END switch case -----
    src.append('}')
    return src


def parseInitJobs(symbfile, jobk):
    addresses = nm_findInstances(symbfile, 'mkenumstr__')
    gdb_loadSymbols(symbfile)
    jobs = []
    for addr in addresses:
        job = gdb_getStructDict(addr, 'struct mkenumstr_job_s')
        jobs.append({'args' : byteify(job), 'meta':{'addr': addr}})

    return jobs

def main():
    print ('---- {} ----'.format(__file__))
    symbfile = envarg.symbfile.get()
    ocfile = envarg.ocfile.get()
    ohfile = envarg.ohfile.get()

    jobs = parseInitJobs(symbfile, 'args')
    oclines = []
    ohlines = []

    for job in jobs:
        args = job['args']
        gdbexpr = args['find'] if args['find'] else args['funcprmtype']
        emnumdefs, defsrcfile = findenums(gdbexpr)

        job['meta']['defsrcfile'] = defsrcfile
        job['enumdefs']   = emnumdefs
        job['enumrepr']   = makeEnumRepr(job)
        oclines.extend(genFuncSrc(job))

    pprint(jobs)
    #pprint(oclines)
    log.debug('ocfile:%s, ohfile: %s', ocfile, ohfile)

    if ocfile is not None:
        ocstr = '\n'.join(oclines)
        log.debug('Writing to file')
        with open(ocfile,'w') as fh: #auto close
                fh.write(ocstr)
    else:
        pprint(oclines)




if __name__ == '__main__':
    main()
