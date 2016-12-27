#from __future__ import print_function
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
import codegen
import gdbtoolz

log = logging.getLogger(os.path.basename(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    disable_existing_loggers=False)


def fullrelpath(p):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisdir, p)


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


def makeEnumRepr(emnumdefs, strstrip=None, exclude=None, **kwargs):
    #log.debug(emnumdefs)
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


def parseInitJobs(symbfile, jobk):
    addresses = nm_findInstances(symbfile, 'mkenumstr__')
    gdb_loadSymbols(symbfile)
    jobs = []
    for addr in addresses:
        job = gdb_getStructDict(addr, 'struct mkenumstr_job_s')
        jobs.append({'args' : byteify(job), 'meta':{'addr': addr}})

    return jobs

def export(srcfile, srclines):
    if not srcfile:
        for line in srclines: print(line)
        return
    srcstr = '\n'.join(srclines)
    log.info('Writing source file %s', srcfile)
    with open(srcfile,'w') as fh: #auto close
            fh.write(srcstr)


def main():
    log.info('-------- GDB --------')

    symbfile = envarg.symbfile.get()
    ocfile = envarg.ocfile.get()
    ohfile = envarg.ohfile.get()

    oclines = []
    ohlines = []
    ohlines.extend(codegen.includeGuardBegin(ohfile))

    gdbtoolz.loadSymbols(symbfile)

    addresses = nm_findInstances(symbfile, 'mkenumstr__')

    for addr in addresses:
        args = gdbtoolz.getStructDict(addr, 'struct mkenumstr_job_s')
        gdbexpr = args['find'] if args['find'] else args['funcprmtype']
        enumdefs, defsrcfile = gdbtoolz.lookupEnums(gdbexpr)
        enumrepr = makeEnumRepr(enumdefs, **args)

        kvcomments = args
        kvcomments['defsrcfile'] = defsrcfile

        ohlines.extend(
            codegen.funcPrototype(kvcomments=kvcomments, term=';\n', **args))

        oclines.extend(
            codegen.funcPrototype(kvcomments=kvcomments, term='\n{', **args))
        oclines.extend(
            codegen.funcSourceBody(enumdefs, enumrepr, **args))

    ohlines.extend(codegen.includeGuardEnd())

    #pprint(jobs)
    #pprint(oclines)
    log.debug('ocfile:%s, ohfile: %s', ocfile, ohfile)

    export(ocfile, oclines)
    export(ohfile, ohlines)



if __name__ == '__main__':
    main()
