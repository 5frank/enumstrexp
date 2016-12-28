#from __future__ import print_function
import gdb
import os
import logging
import re
import subprocess
import tempfile
from pprint import pprint

#needed as python invoked by gdb
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR) #

import envarg
import codegen
import gdbtoolz

log = logging.getLogger(os.path.basename(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr,
    format='%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    disable_existing_loggers=False)


def relToFullPath(p):
    return os.path.join(THIS_DIR, p)


def compileSymbolTable(ifile, searchdirs=[], includes=[]):
    TMP_FILE_PREFIX = 'mkenumstr_tmpfile_'
    tmpc = tempfile.NamedTemporaryFile(
            prefix=TMP_FILE_PREFIX,
            suffix='.c',
            delete=False)
    srcfile = tmpc.name

    tmpo = tempfile.NamedTemporaryFile(
            prefix=TMP_FILE_PREFIX,
            suffix='.o',
            delete=False)
    objfile = tmpo.name

    with open(srcfile,'w') as fh: #auto close
            fh.write('int main(void) { return 0; }')

    log.debug('Creating tmp symbol table %s', objfile)
    cmd = ['gcc', '-o', objfile, srcfile,
        '-O0', '-g', '-g3', '-ggdb', '-std=gnu99', '-Wall',
        '-D', 'MKENUMSTR_COMPILE',
        '-fno-eliminate-unused-debug-types',
        '-include', relToFullPath('mkenumstr.h'),
        '-include', ifile,
        '-I', THIS_DIR
    ]
    for inclfile in includes:
        #cmd.extend(['-I', os.path.abspath(incldir)])
        #cmd.extend(['-I', relToFullPath(incldir)])
        cmd.extend(['-include', inclfile])

    for incldir in searchdirs:
        #cmd.extend(['-I', os.path.abspath(incldir)])
        #cmd.extend(['-I', relToFullPath(incldir)])
        cmd.extend(['-I', incldir])
    #pprint(cmd)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        if out is None: out = ''
        if err is None: err = ''
        print('#error "E: Failed to compile symbol table"')
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        sys.exit(1)
        objfile = None

    log.debug('Removing temp srcfile %s', srcfile)
    os.remove(srcfile)
    return objfile


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


class SrcArgsNamespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

    def __iter__(self):
        for k,v in self.__dict__.items():
            yield k,v

def getSrcArgsList(objfile):
    ''' assumes objfile loaded to gdb prior call '''
    srcargsl = []
    addresses = nm_findInstances(objfile, 'mkenumstr__')

    for addr in addresses:
        srcargsd = gdbtoolz.getStructDict(addr, 'struct mkenumstr_job_s')
        srcargsl.append(SrcArgsNamespace(srcargsd))

    return srcargsl


def doEnum(cliargs, srcargs):
    srcargsd = dict(srcargs)
    gdbexpr = srcargs.find if srcargs.find else srcargs.funcprmtype
    '''
    try:
        ced = gdbtoolz.lookupEnums(gdbexpr, srcargs.mergedefs)
    except LookupError as e:
        log.error('Failed to lookup "%s" %s:%d', gdbexpr, srcargs.filename,
            srcargs.fileline)
        sys.exit(-1)
        raise e #TODO better error message


    enumdefs = ced.members
    enumrepr = makeEnumRepr(enumdefs, **srcargsd)

    kvcomments = srcargsd
    kvcomments['defsrc'] = ced.defsrc
    kvcomments['enumname']  = ced.name
    srclns = []
    if cliargs.oheader:
        srclns.extend(codegen.funcPrototype(
            kvcomments=kvcomments, term=';\n', **srcargsd))
    else:

        srclns.extend(
            codegen.funcPrototype(
                kvcomments=kvcomments, term='\n{', **srcargsd))
        srclns.extend(
            codegen.funcSourceBody(enumdefs, enumrepr, **srcargsd))
    '''
    src = []


    enumsfound = gdbtoolz.lookupEnums(gdbexpr)
    if len(enumsfound) == 0:
        log.error('Failed to lookup "%s" %s:%d', gdbexpr, srcargs.filename,
            srcargs.fileline)
        sys.exit(1)
    if len(enumsfound) > 1 and not srcargs.mergedefs:
        log.error('Multiple enums found "%s" %s:%d', gdbexpr, srcargs.filename,
                    srcargs.fileline)
        sys.exit(2)


    if cliargs.oheader:
        src.extend(codegen.funcDoxyComment(details=srcargsd, **srcargsd))
        src.extend(codegen.funcPrototype(term=';', **srcargsd))
        src.append('') #new line
        return src

    src.extend(codegen.funcDoxyComment(details={}, **srcargsd))
    src.extend(codegen.funcPrototype(term='', **srcargsd))

    src.extend(codegen.funcDefBegin(**srcargsd))
    for ef in enumsfound:
        enumdefs = ef.members
        enumrepr = makeEnumRepr(enumdefs, **srcargsd)
        comments = ['src:{}'.format(ef.defsrc), 'enum: {}'.format(ef.name)]
        src.extend(codegen.multilineComment(comments, 2))
        src.extend(codegen.funcDefCases(enumdefs, enumrepr, **srcargsd))

    src.extend(codegen.funcDefEnd(**srcargsd))

    return src

def main():
    cliargs = envarg.getargs()
    log.setLevel(cliargs.loglevel)
    log.debug('-------- GDB --------')
    log.debug(str(cliargs))

    srclns = []
    if cliargs.includes:
        includes = codegen.includeDirectives(cliargs.includes, cliargs.defundef)
        if cliargs.useguards:
            srclns.extend(codegen.includeGuardBegin(cliargs.outfile))
            srclns.extend(includes)
            srclns.extend(codegen.includeGuardEnd())
        else:
            srclns.extend(includes)

    for ifile in cliargs.ihfile:
        objfile = compileSymbolTable(ifile, cliargs.searchdir, cliargs.includes)
        gdbtoolz.loadSymbols(objfile)
        for srcargs in getSrcArgsList(objfile):
            srclns.extend(doEnum(cliargs, srcargs))
        log.debug('Removing temp file %s', objfile)
        os.remove(objfile)

    if cliargs.outfile:
        #TODO check file
        srcstr = '\n'.join(srclns)
        log.info('Writing source file %s', cliargs.outfile)
        with open(cliargs.outfile,'w') as fh:
            fh.write(srcstr)
    else:
        for line in srclns:
            print(line)

    return 0



if __name__ == '__main__':
    main()
