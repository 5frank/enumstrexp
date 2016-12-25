import subprocess
import os
import logging
import sys
import config


log = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)



def invokegdb(xpath, args=[]):
    #os.environ['SHELL_ARGS'] = str(args)
    os.environ[config.ARGS_ENVVAR] = ' '.join(args)

    cmd = ['gdb', '-n', '-silent', '-batch', '-x', xpath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None
    print (out)
    return 0


def main():
    thisdir = os.path.dirname(os.path.abspath(__file__))
    gdbxpath = os.path.join(thisdir, 'enumstrexp.py')


    args = [
    '-I', '../test',
    '-I', '../test/codegen',
    '-I', '.']

    #args = sys.argv

    #incsfull = [os.path.abspath(p) for p in incs]
    #args, unknownargs = parser.parse_known_args()
    #args = parser.parse_args()
    #print(args)
    #return
    #cCompile(args.searchdir)

    invokegdb(gdbxpath, args)

if __name__ == '__main__':

    main()
