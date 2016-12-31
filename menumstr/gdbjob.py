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


logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr, #allows shell pipe of stdout
    format='%(levelname)s:%(name)s:%(lineno)04d: %(message)s')

class SrcArgsNamespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

    def __iter__(self):
        for k,v in self.__dict__.items():
            yield k,v

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

def makeEnumRepr(cliargs, srcargs, emnumdefs):
    #log.debug(emnumdefs)

    if srcargs.strstrip is not None: # none if srcargs.strstrip == ''
        restrip = re.compile(srcargs.strstrip)
        stripper = lambda x : restrip.sub('', x)

    elif cliargs.stripcommonprefix:
        prefix = os.path.commonprefix(emnumdefs.keys())
        restrip = re.compile('^{}'.format(prefix))
        stripper = lambda x : restrip.sub('', x)

    else:
        stripper = lambda x : x

    if srcargs.exclude:
        reexcl = re.compile(srcargs.exclude)
        excluder = lambda x : reexcl.search(x) is not None
    else:
        excluder = lambda x : False

    enumrepr = {}
    for name, val in emnumdefs.items():
        enumrepr[name] = None if excluder(name) else stripper(name)

    return enumrepr

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

def kvComments(cliargs, srcargsd, gdbexpr):
    srcargsbasename = os.path.basename(srcargsd['filename'])
    d  = {
        'gencfg': '{}:{}'.format(srcargsbasename, srcargsd['fileline']),
        'enum': gdbexpr
    }
    return d
    '''
    'strstrip': str(srcargsd['strstrip'])

    if cliargs.stripcommonprefix:
        d['stripcommonprefix'] = 'Yes'

    ignore = ['filename', 'fileline', 'strstrip', 'funcname',
        'funcprmsize', 'funcprmtype', 'find']
    for k, v in srcargsd.items():
        if k in ignore:
            continue
        if v:
            d[k] = v
    return d
    '''

def doEnum(cliargs, srcargs):
    srcargsd = dict(srcargs)
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

    #if cliargs.oheader:
    details = kvComments(cliargs, srcargsd, gdbexpr)
    h.extend(codegen.funcDoxyComment(details=details, **srcargsd))
    h.extend(codegen.funcPrototype(term=';', **srcargsd))
    h.append('') #new line

    c.extend(codegen.funcDoxyComment(details=details, **srcargsd))
    c.extend(codegen.funcPrototype(term='', **srcargsd))
    c.extend(codegen.funcDefBegin(**srcargsd))

    if len(enumsfound) > 1:
        enumsfound.sort(key=lambda ef: min(ef.members.values()))

    for ef in enumsfound:
        enumdefs = ef.members
        enumrepr = makeEnumRepr(cliargs, srcargs, enumdefs)
        comments = [
            'src:{}'.format(os.path.basename(ef.defsrc)),
            'enum: {} min: {} max:'.format(ef.name, min(ef.members.values()))
            ]
        c.extend(codegen.multilineComment(comments, 2))
        c.extend(codegen.funcDefCases(enumdefs, enumrepr, **srcargsd))

    c.extend(codegen.funcDefEnd(**srcargsd))

    return c, h

def export(outfile, srclines, outtype):
    if outfile == 'stdout':
        if outtype == 'h':
            print('/* -------- MKENUMSTR DECLARATIONS OUTPUT -------- */')
        else:
            print('/* -------- MKENUMSTR DEFINITONS OUTPUT -------- */')
        for line in srclines:
            print(line)
    elif outfile is not None:
        #TODO check file exists
        log.info('Writing source file %s', outfile)
        with open(outfile,'w') as fh:
            fh.write('\n'.join(srclines))
    else:
        log.info('No output destination provides?')

def main():
    cliargs = envarg.getargs()
    #log.setLevel(cliargs.loglevel) # FIXME
    log.debug('-------- GDB --------')
    log.debug(str(cliargs))
    #os.chdir(cliargs.cwd)

    c = []#c code source lines
    h = []#h header declear
    if cliargs.useguards:
        h.extend(codegen.includeGuardBegin(cliargs.outh))

    #definitions likley depends on these headers
    #baseincls = [os.path.basename(fp) for fp in cliargs.inh]
    baseincls = cliargs.inh
    #if cliargs.usedeps: #TODO
    h.extend(codegen.includeDirectives(baseincls))
    c.extend(['#define MKENUMSTR_SOURCE'])
    c.extend(codegen.includeDirectives(baseincls))


    if cliargs.includes:
        includes = codegen.includeDirectives(cliargs.includes)
        c.extend(includes)

    for ih in cliargs.inh:
        objfile = compileSymbolTable(ih, cliargs.searchdir, cliargs.includes)
        gdbtoolz.loadSymbols(objfile)
        for srcargs in getSrcArgsList(objfile):
            _c, _h = doEnum(cliargs, srcargs)
            c.extend(_c)
            h.extend(_h)
        else:
            log.warning('Found nothing to export from %s', ih)
        log.debug('Removing temp file %s', objfile)
        os.remove(objfile)

    if cliargs.useguards:
        h.extend(codegen.includeGuardEnd())

    export(cliargs.outc, c, 'c')
    export(cliargs.outh, h, 'h')

    return 0


if __name__ == '__main__':
    main()
