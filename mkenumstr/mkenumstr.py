from __future__ import print_function
import os
import subprocess
import re
import sys
import argparse
import tempfile
from pprint import pprint
import logging
log = logging.getLogger(os.path.basename(__file__))

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stderr,
    format='%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    disable_existing_loggers=False)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR) #
import envarg


def relToFullPath(p):
    return os.path.join(THIS_DIR, p)

def main():
    envarg.setargs(sys.argv[1:])

    cmd = ['gdb', '-n', '-silent', '-batch', '-x', relToFullPath('gdbjob.py')]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        #log.debug('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return 1
    if out:
        print(out.decode('ascii')) #py3 as subprocess return bytes not str
    if err:
        print(err.decode('ascii')) #py3 as subprocess return bytes not str
    return p.returncode

if __name__ == '__main__':

    main()
