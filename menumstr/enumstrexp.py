"""
Expeort enum symbold name from symbol table (.elf).
Using .elf. or simlar is the only safe way
as enum values might change with defines in makefile and compiler options.
Requires gdb > 7.3 ? for python API

Author: Simon Frank 2016
LICENSE MIT/TBD - mostly a spare time project and
older version might live on github.
"""
from __future__ import print_function
import gdb
import gdb.types
import shlex
import copy
from datetime import datetime
from os.path import basename
from operator import attrgetter
from pprint import pprint # dbg

import os
import re
import sys
import json
import logging
import subprocess
#needed as python invoked by gdb
scriptDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scriptDir) #

import enumstrjob
import gdbtoolz
import config

log = logging.getLogger(__file__)

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)


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
        #print line

    return addrs

def byteify(x):
    ''' python < 3. convert unicode to string '''
    if sys.version_info[0] >= 3:
        return x
    if isinstance(x, dict):
        return {byteify(key): byteify(value)
                for key, value in x.iteritems()}
    elif isinstance(x, list):
        return [byteify(element) for element in x]
    elif isinstance(x, unicode):
        return x.encode('utf-8')
    else:
        return x

def findEnumDefs(jobs, symbfile):
    ''' Modifies callesr copy '''
    gdbtoolz.loadSymbols(symbfile)
    missingDefsCount = 0
    for job in jobs:
        assert(isinstance(job, enumstrjob.EnumStrJob))
        if job.enumdefs: # already have it
            #FIXME check conflicting def
            continue
        ed = gdbtoolz.getEnumDict(job.fromtype)
        if ed is not None:
            job.enumdefs = ed
            job.props['symbolsource'] = str(symbfile)
        else:
            missingDefsCount += 1
    return missingDefsCount

def getJobs(exefile, addresses):
    jobs = []
    for addr in addresses:
        cfg = gdbtoolz.getStructAsDict(addr, 'struct mkenumstr_job_s')
        cfg = byteify(cfg) # python < 3 no unicode. extra sanity
        rettype, prmtype = gdbtoolz.getFuncIOTypes(cfg['funcname'])
        cfg['funcrettype'] = rettype
        cfg['funcprmtype'] = prmtype
        asbitflags = True if cfg['lutype'] == 'BITFLAG2STR' else False
        job = enumstrjob.EnumStrJob(cfg['args'], cfg)
        jobs.append(job)

    return jobs

def fullrelpath(p):
    #if os.path.isabs(p):
    #return p
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisdir, p)

def cCompile(includes=[]):
    #import tempfile
    #tempfile.mkdtemp
    ifile = fullrelpath('main.c')
    ofile = fullrelpath('main.o')
    incl = fullrelpath('menumstr.h')

    cmd = ['gcc', '-o', ofile, ifile,
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


'''
_parser = argparse.ArgumentParser(add_help=False)

_parser.add_argument('-v', '--verbose',
    action='store_true',
    help='Verbose output')
'''

def getLauncherVar(varname):
    ''' retrive variable passsed to gdb from launcer script '''
    ev = str(gdb.parse_and_eval(varname))
    ev = ev[1:-1] # remove quotes added
    return ev


from pprint import pprint
import shlex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-I', '--searchdir',
    type=str,
    action='append',
    help='Include directory')

def main():
    '''
    cliargstr = getLauncherVar('$SHELL_ARGS')
    '''
    cliargstr = os.environ[config.ARGS_ENVVAR]
    args = parser.parse_args(shlex.split(cliargstr))
    cCompile(args.searchdir)
    print (args)
    #return 0
    #print(getLauncherVar('$SHELL_ARGS'))
    symbfile = config.INIT_SYMFILE #getLauncherVar('$SYMB_OBJ')
    #symbfile = os.path.abspath('main.o') #getLauncherVar('$SYMB_OBJ')
    gdbtoolz.loadSymbols(symbfile)
    jobaddr = nm_findInstances(symbfile, 'mkenumstr_job')
    if not jobaddr:
        log.error('Failed to find descriptor addresses')
        return 1

    log.debug('job structs addr: {}'.format(jobaddr))

    jobs = getJobs(symbfile, jobaddr)

    #return 0
    #priority in same order as array
    symbfiles = [symbfile]
    missingDefs = 0
    for symbf in symbfiles:
        missingDefs = findEnumDefs(jobs, symbf)
    if missingDefs:
        log.error('Failed to looooookup %d enums', missingDefs)
        #TODO print which and exit

    for job in jobs:
        s = job.renderCode()
        print (s)
        print( str(job.enumrepr))

    pprint(jobs)
    #mkCCode(jobs)



    '''
    exepath = cCompile(os.path.join(scriptDir, 'main.c'))
    assert(exepath)
    jobaddr = getJobAddr(exepath)
    assert(jobaddr)
    '''


if __name__ == '__main__':

    main()
    #args = getShellArgs()
    #mmain.run(args)
