from __future__ import print_function
import os
import subprocess
import sys

import logging
log = logging.getLogger(os.path.basename(__file__))

import envarg

def main():
    '''
    it is currently only possible to invoke the ptyhon gdb api _from_
    within gdb, this requires some hacks, like passing argumetns as a shell
    environment variable.
    '''
    envarg.setargs(sys.argv[1:]) # used by the gdb process.

    thisdir = os.path.dirname(os.path.abspath(__file__))
    xpath = os.path.join(thisdir,('gdbjob.py'))
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
