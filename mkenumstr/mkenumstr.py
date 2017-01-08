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

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR)
import envarg

def main():
    '''
    Currently, can only invoke python from GDB.
    '''
    envarg.setargs(sys.argv[1:]) # used by the gdb process.

    xpath = os.path.join(THIS_DIR,('gdbjob.py')
    cmd = ['gdb', '-n', '-silent', '-batch', '-x', xpath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        pass # errors should already been printed by the subprocess
    if out:
        print(out.decode('ascii')) # py3 as subprocess return bytes not str
    if err:
        print(err.decode('ascii')) # py3 as subprocess return bytes not str

    return p.returncode

if __name__ == '__main__':
    sys.exit(main())
