from __future__ import print_function
import os
import subprocess
import re
import sys
import argparse
import tempfile
from pprint import pprint
import logging
log = logging.getLogger(__file__)

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)

scriptDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scriptDir) #
import envarg

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def fullrelpath(p):
    return os.path.join(THIS_DIR, p)

def compileSymbolTable(ifile, includes=[]):
    TMP_FILE_PREFIX = 'mkenumstr_tmpfile_'
    #srcfile = fullrelpath('main.c')
    #objfile = fullrelpath('main.o')
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
        '-include', fullrelpath('mkenumstr.h'),
        '-include', ifile,
        '-I', THIS_DIR
    ]

    for incldir in includes:
        cmd.extend(['-I', os.path.abspath(incldir)])

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        objfile = None

    log.debug('Removing temp srcfile %s', srcfile)
    os.remove(srcfile)
    return objfile

def gdb_invokeMkJobs(symbfile, ocfile, ohfile=None):
    envarg.symbfile.set(fullrelpath(symbfile))
    envarg.ocfile.set(fullrelpath(ocfile) if ocfile else None)
    envarg.ohfile.set(fullrelpath(ohfile) if ohfile else None)

    #os.environ['SHELL_ARGS'] = str(args)
    #os.environ[config.ARGS_ENVVAR] = ' '.join(args)
    xpath=fullrelpath('gdbmkenumstr.py')
    cmd = ['gdb', '-n', '-silent', '-batch', '-x', xpath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None
    print(out.decode('ascii')) #py3 as subprocess return bytes not str
    return p.returncode


parser = argparse.ArgumentParser()

parser.add_argument('-i', '--ihfile',
    type=str,
    action='append',
    default=[],
    help='input file. header to create source from')

parser.add_argument('-oc', '--ocfile',
    type=str,
    help='output source file to be generated. ')


parser.add_argument('-oh', '--ohfile',
    type=str,
    help='Optional output header file to be generated.')


parser.add_argument('-I', '--searchdir',
    type=str,
    action='append',
    default=[],
    help='Directory to search for includes. same as gcc -I arg')


parser.add_argument('-s', '--symboltable',
    type=str,
    action='append',
    default=[],
    help='Extra symbol table(s) readable by gdb (.elf, .o. out, etc)'\
         'where enums can be found. assumes compiled with debug symbols')

def main():

    args = parser.parse_args()
    for ifile in args.ihfile:
        objfile = compileSymbolTable(ifile)

        gdb_invokeMkJobs(objfile, args.ocfile, args.ohfile)
        log.debug('Removing temp file %s', objfile)
        os.remove(objfile)


if __name__ == '__main__':

    main()
