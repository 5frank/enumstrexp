'''
Module needed to pass arguments from launcher script to gdb.
might be removed in future when gdb API can handle thus better
'''
import os
import shlex
import argparse
import logging
log = logging.getLogger(os.path.basename(__file__))


ENV_CLIARGS = 'MKENUMSTR_CLIARGS'
ENV_ORGCWD = 'MKENUMSTR_ORGCWD'

VERBOSE_TO_LOGLVL = [
    logging.WARNING,
    logging.INFO,
    logging.DEBUG]

parser = argparse.ArgumentParser()


parser.add_argument('-i', '--ihfile',
    type=str,
    action='append',
    default=[],
    help='input file(s). header to create source from')

parser.add_argument('-of', '--outfile',
    type=str,
    help='Output file to be generated. Output is sent to stdout if not set')

parser.add_argument('-I', '--searchdir',
    type=str,
    action='append',
    default=[],
    help='Directory to search for includes. same as gcc -I arg')

parser.add_argument('--includes',
    type=str,
    action='append',
    default=[],
    help='Comma or line break spearated list of includes')

parser.add_argument('--defundef',
    type=str,
    default=[],
    help='Wrap all includes with this. solves poluted namespace etc')


parser.add_argument('--oheader',
    action='store_true',
    default=False,
    help='Output header')


parser.add_argument('--useguards',
    action='store_true',
    default=False,
    help='Use include guards')

parser.add_argument('-v', '--verbose',
    action='count',
    default=0,
    help="Verbose Output. -v(vv)...")

if 'TODO' == 'DONE':
    parser.add_argument('-s', '--symboltable',
        type=str,
        action='append',
        default=[],
        help='Extra symbol table(s) readable by gdb (.elf, .o. out, etc)'\
             'where enums can be found. assumes compiled with debug symbols')


def _splitArgList(argList):
    ls = []
    if not argList:
        return ls
    for itm in argList.replace('\n', ',').split(','):
        if itm: ls.append(itm)
    return ls

def _splitListOfArgList(listOfArgLists):
    ls = []
    for x in listOfArgLists:
        ls.extend(_splitArgList(x))
    return ls

def setargs(argv):
    ''' argv excluding argv[0] i.e. script name '''
    argstr = ' '.join(argv)
    #argstr = argstr.replace('"', '\"')
    log.debug(argstr)
    os.environ[ENV_CLIARGS] = argstr
    os.environ[ENV_ORGCWD] = os.getcwd()

def getargs():
    if ENV_CLIARGS not in os.environ:
        return None
    argstr = os.environ[ENV_CLIARGS]
    #log.debug(argstr)
    args = parser.parse_args(shlex.split(argstr))

    args.includes = _splitListOfArgList(args.includes)
    args.defundef = _splitArgList(args.defundef)

    verboseCount = min(args.verbose, len(VERBOSE_TO_LOGLVL)-1) #clamp
    args.loglevel = VERBOSE_TO_LOGLVL[verboseCount]
    return args

def cwdfullpath(p):
    return os.path.join(os.environ[ENV_ORGCWD], p)
