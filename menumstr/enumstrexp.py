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


log = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format='%(asctime)s:%(levelname)s:%(name)s:%(lineno)04d: %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    disable_existing_loggers=True)


def rtassert(condition, fmt='', *args):
    if not condition:
        log.error(fmt, args) # TODO critical?
        raise AssertionError(fmt % args)

def rtassert_path(fpath):
    rtassert(os.path.exists(fpath), 'No such file %s', fpath)


def gdb_defSource(symbName):
    """ source file and path where enum is defined.
       Fails if symbName is enum member."""
    r = gdb.execute('info types ^'+symbName +'$', False, True)
    for l in r.splitlines():
        if l.startswith('File'):
            return l.strip().lstrip('File').rstrip(":")
    return None



def gdbGetEnumDict(enumId, scope=None):
    log.debug('Looking up "%s"', enumId)
    t = None
    def isEnum(t):
        if t == None: return False
        ts = t.strip_typedefs()
        if ts.code == gdb.TYPE_CODE_ENUM: return True
        return False
    # Type from enum typedef id
    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(enumId))
        if not isEnum(t):
            return None
    except RuntimeError:
        # Try find type from enum member name
        try:
            t = gdb.parse_and_eval(enumId).type
            if not isEnum(t):
                return None
        except RuntimeError:
            return None
    # success, enum instance found
    bt = gdb.types.get_basic_type(t)
    enumDict =  gdb.types.make_enum_dict(bt)
    return enumDict


def gdbLoadSymbolsFrom(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    rtassert(not r, 'gdb.execute returned %s', str(r))


def gdbGetFuncInfo(func, srcfile=''):
    '''
    r = gdb.execute('info functions {}'.format(func), False, True)
    for line in r.split('\n'):
        if func in line:
    '''


    try:
        t = gdb.types.get_basic_type(gdb.lookup_type(func))
    except RuntimeError:
        # Try find type from enum member name
        try:
            t = gdb.parse_and_eval(func).type
            t = gdb.types.get_basic_type(t)
        except RuntimeError:
            return None, None
    s = str(t)
    m = re.search(r'(.*?)\((.*?)\)', s)
    rettype = m.group(1)
    prmtype = m.group(2)
    return rettype, prmtype
    #return m #str(m.group(0))



def getJobAddr(symbfile, prefix='mkenumstr_job'):
    '''
    gdb will fail to retrive theses. why?
    like $ nm -C main.o | grep $PREFIX | cut -d ' ' -f 1
    but a little bit more secure. sigh
    '''
    rtassert_path(symbfile)
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


def getJobs(exefile, addresses):
    def byteify(x):
        if isinstance(x, dict):
            return {byteify(key): byteify(value)
                    for key, value in x.iteritems()}
        elif isinstance(x, list):
            return [byteify(element) for element in x]
        elif isinstance(x, unicode):
            return x.encode('utf-8')
        else:
            return x

    rtassert_path(exefile)

    cmd = [exefile]
    cmd.extend(addresses)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    if p.returncode != 0:
        log.error('cmd %s returned %d. %s', ' '.join(cmd), p.returncode, err)
        return None

    confs = json.loads(out)
    if 0: # python < 3 no unicode. extra sanity
        confs = byteify(confs) #

    for i in xrange(len(confs)):
        #for cfg in confs.iteritem:
        cfg = byteify(confs[i]) # python < 3 no unicode. extra sanity
        rettype, prmtype = gdbGetFuncInfo(cfg['func'])
        cfg['funcrettype'] = rettype
        cfg['funcprmtype'] = prmtype

        confs[i] = {'conf' : cfg, 'exportnfo' :{} }

    return confs

def lookupEnumDefs(jobs, symbfile):
    ''' Modifies callesr copy '''
    gdbLoadSymbolsFrom(symbfile)
    missingDefsCount = 0
    enumdk = 'enumdefs'
    for job in jobs:
        if enumdk not in job: # or job[enumdk] is None:
            ed = gdbGetEnumDict(job['conf']['enumid'])
            if ed is not None:
                job[enumdk] = ed
                job['exportnfo']['symbolsource'] = str(symbfile)
            else:
                missingDefsCount += 1
    return missingDefsCount

#---------alter for export ----------------------------------------------
def findCommonPrefix(members, maxIgnored=1, minMatchLen=2):
    '''Given a list of strings, returns the longest common string,
    ignoring max N unmatched strings set by param, or empty string'''
    membersMaxLen =  len(max(members, key=len))
    commons = [''] * membersMaxLen
    for i in range(0, membersMaxLen):
        ignored = 0
        d = {}
        for s in members: # N:th char for all in list
            if i >= len(s):
                ignored += 1
                continue
            c = s[i] # char
            if not c in d:
                d[c] = 1
            else:
                d[c] += 1
        ignored += len(d) - 1 # always one or more item(s) in d
        if ignored <= maxIgnored:
            commons[i] = max(d, key=d.get) # add winner
        else:
            break
    res = ''.join(commons)
    if len(res) < minMatchLen:
        res = ''
    return res

def alterMemberNames(job):
    alternfo = []
    em = job['enumdefs'].copy() #
    if job['conf']['lstrip']:
        prefix = findCommonPrefix(em.keys())
        if prefix:
            reExpr = '^{}'.format(prefix)
            alternfo.append(reExpr)
            reObj = re.compile(reExpr)
            em = {reObj.sub('', k):v for (k,v) in em.iteritems()}

    if job['conf']['rstrip']:
        raise NotImplementedError('TODO rstrip automagic')

    refmt = job['conf']['refmt']
    if refmt:
        pass

    job['exportnfo']['regexps'] = alternfo
    return em

def mkInvertDict(job):
    vald = {}
    duplicates = 0
    for name, val in job['enumrepr'].items():
        #val = int(val)
        if val in vald:
             vald[val] += '==' + name
             duplicates += 1
        vald[val] = name
    job['exportnfo']['duplicates'] = duplicates
    #>>> [k for k, v in rev_multidict.items() if len(values) > 1]
    return vald

def mkStringRepr(jobs):
    ''' Modifies callesr copy '''
    for job in jobs:
        if 'enumdefs' not in job:
            log.warning('No defs for {}'.format(job))
            continue

        altrepr = alterMemberNames(job)
        duplicates = 0
        enumrepr = {}
        for name, val in altrepr.items():
            #val = int(val)
            if val in enumrepr:
                 vald[val] += '==' + name
                 duplicates += 1
            enumrepr[val] = name
        job['enumrepr'] = enumrepr
        job['exportnfo']['duplicates'] = duplicates

    return jobs

#----------------------generate code --------------------------



def mkCCodeFuncSwitchCase(job, prmname='x', tablvl=1, usedefs=True, default='<?>'):
    if 'enumrepr' not in job:
        return default #FIXME

    tabs = lambda n : n * '  ' #TODO from config
    reprvkd = job['enumrepr']
    defsvkd = {v: k for k, v in job['enumdefs'].iteritems()}

    asbitflags = job['conf']['bitflags']

    s = ''
    n = tablvl # tab level
    s += '{}switch({})\n'.format(tabs(n), prmname)
    s += '{}{{\n'.format(tabs(n))# escpae '{' with '{{'
    n += 1
    for emval in sorted(reprvkd.keys()):
        emstr = reprvkd[emval]
        emdef = defsvkd[emval]
        caselbl = emdef if usedefs else emval
        caselbl = 'BITPOS32({})'.format(caselbl) if asbitflags else caselbl

        s += '{}case {}:\n'.format(tabs(n), caselbl)
        s += '{}return "{}"; break;\n'.format(tabs(n+1), emstr)

    s += '{}default:\n'.format(tabs(n))
    s += '{}return "{}"; break;\n'.format(tabs(n+1), default)

    s += tabs(n-1) + '}\n'
    return s


def mkCCodeFunc(job, outfile=''):

    c = job['conf']
    if c['bitflags']:
        prmname = 'bitpos'
        brief = 'Enum bit flag index to string lookup'
        param = ' - bit position index representing a enum flag.'
    else:
        prmname = 'value'
        brief = 'Enum value to string lookup.'
        param = ' - enum value.'

    s =  '/**\n'
    s += ' * @brief {}\n'.format(brief)
    s += ' * @note  Do not modify! Auto generated code.\n'
    s += ' * @param {} - {}\n'.format(prmname, param)
    for k, v in job['exportnfo'].items():
        if v:
            s += ' *    {}:{}\n'.format(k, v) #FIXME escape c '*/' etc
    s += ' */\n'

    fmt = '{} {}({} {})\n'
    s += fmt.format(c['funcrettype'], c['func'], c['funcprmtype'], prmname)
    s += '{\n'
    s += mkCCodeFuncSwitchCase(job)
    s += '}\n'
    return s


def mkCCode(jobs, outfile=''):
    for job in jobs:
        s = mkCCodeFunc(job)
        print (s)



'''
_parser = argparse.ArgumentParser(add_help=False)

_parser.add_argument('-c', '--cfgfile',
    nargs='+',
    metavar='FILE',
    help='Run conf(s) file.')

_parser.add_argument('-h', '--help',
    action='store_true',
    help='Show help.')

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

def main():
    '''
    cliargstr = getLauncherVar('$SHELL_ARGS')
    args = _parser.parse_args(shlex.split(cliargstr))
    '''

    symbfile = getLauncherVar('$SYMB_OBJ')
    gdbLoadSymbolsFrom(symbfile)
    jobaddr = getJobAddr(symbfile)
    rtassert(jobaddr, 'Failed to find descriptor addresses')
    log.debug('job structs addr: {}'.format(jobaddr))

    jobs = getJobs(symbfile, jobaddr)

    #priority in same order as array
    symbfiles = [symbfile]
    missingDefs = 0
    for symbf in symbfiles:
        missingDefs = lookupEnumDefs(jobs, symbf)
    if missingDefs:
        log.error('Failed to looooookup %d enums', missingDefs)
        #TODO print which and exit

    mkStringRepr(jobs)
    pprint(jobs)
    mkCCode(jobs)



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
