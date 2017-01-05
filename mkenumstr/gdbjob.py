#from __future__ import print_function
import gdb
import os
import logging
import re
import subprocess
import tempfile
import sys
from pprint import pprint

#needed as python invoked by gdb
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR) #

import envarg
import codegen
import gdbtoolz

log = logging.getLogger(os.path.basename(__file__))

class SrcArgsNamespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

    def __iter__(self):
        for k,v in self.__dict__.items():
            yield k,v
    def __str__(self):
        return str(self.__dict__)


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
        '-D', 'MKENUMSTR_SOURCE',
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

def getSrcArgsList(objfile):
    ''' assumes objfile loaded to gdb prior call '''
    srcargsl = []
    addresses = nm_findInstances(objfile, 'mkenumstr__')

    for addr in addresses:
        srcargsd = gdbtoolz.getStructDict(addr, 'struct mkenumstr_job_s')
        srcargsl.append(SrcArgsNamespace(srcargsd))
    #sort to same order as gencdg
    srcargsl.sort(key=lambda srcargs: srcargs.fileline)
    return srcargsl

def doEnum(cliargs, srcargs):
    gdbexpr = srcargs.find if srcargs.find else srcargs.funcprmtype
    c = []
    h = []
    enumsfound = gdbtoolz.lookupEnums(gdbexpr)
    if len(enumsfound) == 0:
        log.error('Failed to lookup "%s" %s:%d', gdbexpr, srcargs.filename,
            srcargs.fileline)
        sys.exit(1)

    if len(enumsfound) > 1 and not srcargs.mergedefs:
        log.error('Multiple enums found "%s" %s:%d', gdbexpr, srcargs.filename,
                    srcargs.fileline)
        sys.exit(2)

    if len(enumsfound) > 1:
        enumsfound.sort(key=lambda ef: min(ef.members.values()))

    cgesparams = {}
    cgesparams['doxydetails'] = [
        'gencfg: {}:{}'.format(
            os.path.basename(srcargs.filename), srcargs.fileline),
        'enum: {}'.format(gdbexpr)
    ]
    cgesparams.update(dict(srcargs))
    cgesparams.update(vars(cliargs))
    cgesfunc = codegen.EnumStrFunc(**cgesparams)

    for ef in enumsfound:
        cgesfunc.addEnums(ef.members, ef.defsrc, ef.name)

    return cgesfunc.generate()

def export(outfile, srclines, outtype):
    if not outfile:
        log.info('No output destination provides?')
        if outtype == 'h':
            print('/* -------- MKENUMSTR DECLARATIONS OUTPUT -------- */')
        else:
            print('/* -------- MKENUMSTR DEFINITONS OUTPUT -------- */')
        for line in srclines:
            print(line)
    else:
        #TODO check file exists
        log.info('Writing source file %s', outfile)
        with open(outfile,'w') as fh:
            fh.write('\n'.join(srclines))


def main():
    cliargs = envarg.getargs()
    #log.setLevel(cliargs.loglevel) # FIXME

    logging.basicConfig(
        level=cliargs.loglevel, #logging.DEBUG,
        stream=sys.stderr, #allows shell pipe of stdout
        format='mkenumstr:%(levelname)s:%(name)s:%(lineno)04d: %(message)s')

    log.debug('-------- GDB --------')
    log.debug(str(cliargs))
    #os.chdir(cliargs.cwd)

    c = []#c code source lines
    h = []#h header declear

    h.extend(codegen.doxyFileComments(cliargs.outh))
    c.extend(codegen.doxyFileComments(cliargs.outc))
    inclguard = codegen.IncludeGuard(cliargs.outh)
    if cliargs.useguards:
        h.extend(inclguard.guardBegin())

    #definitions likley depends on these headers
    baseincls = [os.path.basename(fp) for fp in cliargs.inh]
    #baseincls = cliargs.inh
    h.extend(codegen.includeDirectives(baseincls))
    c.extend(['#define MKENUMSTR_SOURCE'])
    c.extend(codegen.includeDirectives(baseincls))

    if cliargs.includes:
        includes = codegen.includeDirectives(cliargs.includes)
        c.extend(includes)

    for ih in cliargs.inh:
        objfile = compileSymbolTable(ih, cliargs.searchdir, cliargs.includes)
        gdbtoolz.loadSymbols(objfile)
        srcargsList = getSrcArgsList(objfile)
        for srcargs in srcargsList:
            log.debug(srcargs)
            _c, _h = doEnum(cliargs, srcargs)
            c.extend(_c)
            h.extend(_h)
        if not srcargsList:
            log.warning('Found nothing to export from %s', ih)
        log.debug('Removing temp file %s', objfile)
        os.remove(objfile)

    if cliargs.useguards:
        h.extend(inclguard.guardEnd())

    export(cliargs.outc, c, 'c')
    export(cliargs.outh, h, 'h')

    return 0


if __name__ == '__main__':
    main()
