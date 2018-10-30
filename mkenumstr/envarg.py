'''
Module needed to pass arguments from launcher script to gdb.
might be removed in future when gdb API can handle this better
'''
import os
import shlex
import argparse
import logging
log = logging.getLogger(os.path.basename(__file__))


ENV_CLIARGS = 'MKENUMSTR_CLIARGS'
ENV_ORGCWD = 'MKENUMSTR_ORGCWD'


parser = argparse.ArgumentParser()

parser.add_argument('-i', '--infile',
    type=str,
    action='append',
    default=[],
    help='Symbol table. .elf, .o')

parser.add_argument('-o', '--outfile',
    type=str,
    default=None,
    help='Output file path. Default to stdout if not set')


parser.add_argument('-e', '--enum',
    type=str,
    action='append',
    default=[],
    help='Enum(s) to export. Expression or exact name.')

parser.add_argument('-v', '--verbose',
    action='count',
    default=0,
    help='Verbose Output. -v(vv)...')

#TODO
'''
parser.add_argument('-f', '--format',
    type=str,
    choices=['json', 'txt', 'xml'],
    default='json',
    help='Enum(s) to export. Expression or exact name.')



parser.add_argument('--strict',
    default=False,
    help='Strict rules');
'''

def setargs(argv):
    ''' argv excluding argv[0] i.e. script name '''
    argstr = ' '.join(argv)
    #argstr = argstr.replace('"', '\"')

    os.environ[ENV_CLIARGS] = argstr
    os.environ[ENV_ORGCWD] = os.getcwd()

def getargs():
    if ENV_CLIARGS not in os.environ:
        return None
    argstr = os.environ[ENV_CLIARGS]
    #log.debug(argstr)
    args = parser.parse_args(shlex.split(argstr))
    args.loglevel = logging.DEBUG if args.verbose else logging.INFO
    if len(args.enum):
        pass # TODO
    args.cwd = os.environ[ENV_ORGCWD]

    return args

def cwdfullpath(p):
    return os.path.join(os.environ[ENV_ORGCWD], p)

