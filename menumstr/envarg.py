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

parser.add_argument('-ih', '--inh',
    type=str,
    action='append',
    default=[],
    help='Input header file(s) with instructions to generate source from')


parser.add_argument('-oc', '--outc',
    type=str,
    default='stdout',
    help='Generated definitions output destination.'\
        ' i.e. function body etc '\
        ' that typically goes in a source fle with a .c suffix')

parser.add_argument('-oh', '--outh',
    type=str,
    default='',
    help='Generated declrarations output destination.'\
        ' i.e. exposed prototypes and defines' \
        ' that typically goes in a header with a .h suffix')

parser.add_argument('-I', '--searchdir',
    type=str,
    action='append',
    default=[],
    help='Directory to search for includes. '\
        'Same as gcc -I arg but value must be separated with space.')

parser.add_argument('--includes',
    type=str,
    action='append',
    default=[],
    help='Comma or line break spearated list of includes')

parser.add_argument('--stripcommonprefix',
        action='store_true',
        default=False,
    help='Strip common prefix in string representation of all enum members. '\
        'This option can be overrided by the .stripstr param in macro param. '\
        'Might give undesirable results if number of enum members is small')

parser.add_argument('--nodeps',
    action='store_true',
    default=False,
    help='Remove/reduce dependencies on enum definitons TODO') #TODO

parser.add_argument('--noinclguards',
    action='store_true',
    default=False,
    help='Do not use include guards in --outh output.'\
        ' Useful if --outh="stdout" and result is appended to file.')

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

if 'REMOVE' == 'LATER':
    parser.add_argument('--defundef',
        type=str,
        action='append',
        default=[],
        help='Wrap all includes with this. solves poluted namespace etc.'\
            'syntax examples: --defundef="FOO=123" --defundef="BAR"')

    parser.add_argument('-of', '--outfile',
        type=str,
        help='Output file to be generated. Output is sent to stdout if not set')

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


def _parseDefUndefs(defundefs):
    '''
    Convert list like ['FOO=123', 'BAR'] to dict {'FOO':123, 'BAR':''}
    Bad names, with spaces etc, should throw error at compile time.
    '''
    d = {}
    for du in defundefs:
        du = du.strip()
        if '=' in du:
            toks = du.split('=')
            if ' ' in toks[0]:
                raise ValueError #TOOD
            k = toks[0]
            v = toks[1] #empty sting if noting after '='
        elif ' ' in du:
            raise ValueError #TOOD
        else:
            k = du
            v = ''
        d[k] = v

    return d

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

    args.includes = _splitListOfArgList(args.includes)
    #args.defundef = _parseDefUndefs(args.defundef)
    # reverse some flags for easier to read code 'stay positive'
    args.usedeps = False if args.nodeps else True
    args.useguards = False if args.noinclguards else True
    args.cwd = os.environ[ENV_ORGCWD]

    verboseCount = min(args.verbose, len(VERBOSE_TO_LOGLVL)-1) #clamp
    args.loglevel = VERBOSE_TO_LOGLVL[verboseCount]
    return args

def cwdfullpath(p):
    return os.path.join(os.environ[ENV_ORGCWD], p)
