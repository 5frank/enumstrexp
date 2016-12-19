import subprocess
import os
import logging
import sys
import config
import argparse


log = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)


def cCompile(includes=[]):
    #import tempfile
    #tempfile.mkdtemp

    # TODO safe tempfile
    #gcc -o $PROG_NAME.o $PROG_NAME.c -lm -ldl -O0 -g3 -ggdb -std=gnu99 -Wall \
    #-export-dynamic -fvisibility=hidden -fno-eliminate-unused-debug-types

    #objName = os.path.filename(srcName) + '.o'
    #src = os.path.abspath(p)
    #srco = '/tmp/main.o'
    cmd = ['gcc', '-o', config.INIT_SYMFILE, 'main.c',
    '-O0', '-g3', '-ggdb', '-std=gnu99', '-Wall',
    '-fno-eliminate-unused-debug-types']

    for incldir in includes:
        cmd.extend(['-I', os.path.abspath(incldir)])

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None

    return 0


def startGdb(args=[]):
    #os.environ['SHELL_ARGS'] = str(args)

    cmd = ['gdb', '-n', '-silent', '-batch',
        '-x', os.path.abspath('enumstrexp.py')
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None
    print (out)
    return 0


parser = argparse.ArgumentParser()
parser.add_argument('-I', '--searchdir',
    type=str,
    action='append',
    help='Include directory')


def main():
    incs = [
    '-I', '../test',
    '-I', '../test/codegen',
    '-I', '.']
    os.environ[config.ARGS_ENVVAR] = ' '.join(incs)
    #incsfull = [os.path.abspath(p) for p in incs]
    #args, unknownargs = parser.parse_known_args()
    #args = parser.parse_args()
    #print(args)
    #return
    #cCompile(args.searchdir)

    startGdb(sys.argv)

if __name__ == '__main__':
    main()
