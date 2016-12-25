import gdb
import os
import logging
import subprocess
from pprint import pprint

log = logging.getLogger(__file__)

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)


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


def gdb_getStrAry(instance):
    ary = []
    for i in xrange(0,7): # in instance: #.type.fields(): FIXME
        v = instance[i]
        v = str(v.string())
        if v.endswith('""'):
            v = v.rstrip('""') # FIXME why ""?
        if v:
            ary.append(v)
    return ary

def gdb_getStructDict(addr, structtype, scope=''):

    try:
        jobtype = gdb.lookup_type(structtype)
        jobaddr = gdb.Value(long(addr, 16))
        jobptr = jobaddr.cast(jobtype.pointer())
        jobinstance = jobptr.dereference()

        job = {}
        job['meta_addr'] = str(hex(int(jobaddr)))
        for field in jobinstance.type.fields():
            fname = field.name
            #log.debug(fname)
            ftype = field.type
            fval = jobinstance[fname]
            c = fval.type.code
            if c == gdb.TYPE_CODE_PTR:
                if fval:
                    v = str(fval.string())#.dereference()
                    #v = v.fetch_lazy()
                    #v = v.string()
                    if v.startswith('"') and v.endswith('"'):
                        v = v.strip('"')
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


def gdb_loadSymbols(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    assert(not r) #, 'gdb.execute returned %s', str(r))


def isenumtype(t):
    if t == None: return False
    ts = t.strip_typedefs()
    if ts.code == gdb.TYPE_CODE_ENUM: return True
    return False

def getEnumDict(enumid):
    t = None
    # Type from enum typedef id
    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(enumid))
        if not isenumtype(t):
            raise LookupError('\'' + enumid + '\' is not a enum')
    except RuntimeError:
        # Try find type from enum member name
        try:
            t = gdb.parse_and_eval(enumid).type
            if not isenumtype(t):
                raise LookupError('\'' + enumid + '\' is not a enum')
        except RuntimeError:
            raise LookupError('No enum found from :', enumid)
    # success, enum instance found
    bt = gdb.types.get_basic_type(t)
    enumsbyname = gdb.types.make_enum_dict(bt)
    enumsbyval = {}
    return enumsbyname

def findenums(findexpr):
    enumsbyval = {}

    r = gdb.execute('info types {}'.format(findexpr), False, True)
    #suspects
    for line in r.splitlines():
        if line.startswith('File'):
            continue

        x = line.rstrip(';').split()
        if 'enum' not in x:
            continue

        i = x.index('enum')
        if len(x) < (i+1):
            print('ignoring line "{}"'.format(line))
            continue
        enumtype = x[i] + ' ' + x[i+1]

        try:
            print('Looking up "{}"'.format(enumtype))
            ed = getenumbyname(enumtype)
        except LookupError:
            print('igoring line 2 "{}"'.format(line))
            continue

        for name, val in ed.iteritems():
            if name.startswith('_'):
                print('ignoring enum "{}"'.format(name))
                continue

            val = int(val)
            if val in enumsbyval:
                dup = enumsbyval[val]
                print('E: duplicate values: "{}" == "{}"'.format(name, dup))
            enumsbyval[val] = name

    return enumsbyval

def fullrelpath(p):
    #if os.path.isabs(p):
    #return p
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisdir, p)


def parse(symbfile):
    addresses = nm_findInstances(symbfile, 'mkenumstr__')
    gdb_loadSymbols(symbfile)
    jobs = []
    for addr in addresses:
        job = gdb_getStructDict(addr, 'struct mkenumstr_job_s')
        jobs.append(byteify(job))

    return jobs

def main():
    print ('---- {} ----'.format(__file__))
    symbfile = os.environ['MKENUMSTR_SYMB_FILE']
    jobs = parse(symbfile)
    for job in jobs:
        if not job['find_expr'] is None:
            gdbexpr = job['find_expr']
        else:
            gdbexpr = job['func_prmt']
        print gdbexpr
        job['enums'] = getEnumDict(gdbexpr)
    pprint(jobs)


if __name__ == '__main__':
    main()
