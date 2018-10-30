#from __future__ import print_function
import gdb
import os
import logging
import re
#import subprocess
import sys
import json

from collections import OrderedDict
from operator import itemgetter

# needed as python invoked by gdb
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR) #
import envarg


log = logging.getLogger(os.path.basename(__file__))


class EnumInfo(object):

    def __init__(self, members={}, expr='', defsrc='', name=''):
        self.members = members
        self.expr = expr
        self.defsrc = defsrc
        self.name = name

    def todict(self):
        d = {}
        d['source'] = self.defsrc
        d['name'] = self.name
        d['expr'] = self.expr
        d['members'] = OrderedDict(
                sorted(self.members.items(), key=itemgetter(1)))
        return d


def loadSymbols(fpath):
    r = gdb.execute('file ' + fpath, False, True)
    assert(not r) #, 'gdb.execute returned %s', str(r))

def isEnumType(t):
    if t is None:
        return False
    ts = t.strip_typedefs()
    if ts.code == gdb.TYPE_CODE_ENUM:
        return True
    return False


def getBasicType(enumTypeName):
    try:
        t = gdb.lookup_type(enumTypeName)
        return gdb.types.get_basic_type(t)
    except RuntimeError:
        pass
    # Try find type from enum member name
    try:
        t = gdb.parse_and_eval(enumTypeName).type
        return gdb.types.get_basic_type(t)
    except RuntimeError:
        pass

    return None

def getDefSource(symbName):
    ''' 
    source file and path where enum is defined.
    Fails if symbName is enum member.
    '''
    r = gdb.execute('info types ^'+symbName +'$', False, True)
    for l in r.splitlines():
        if l.startswith('File'):
            s = l.strip().lstrip('File').rstrip(':')
            return s.strip()
    return None


def getEnums(expr, strict=False):
    log.debug('expr "%s"', expr)

    # first tryexact
    btype = getBasicType(expr)
    if btype is not None and isEnumType(btype):
        log.debug('Found exact type "%s"', expr)
        members = gdb.types.make_enum_dict(btype)
        defsrc = getDefSource(expr)
        name = btype.tag if btype.tag is not None else btype.name
        return [EnumInfo(members, expr, defsrc, name)]
        #return enumdefs, defsrcfile
    enumsd = {}

    expr = re.sub('^enum ', '', expr) # strip prefix if present

    # expr = expr.strip()
    # if not expr.startswith('^'):
        # expr = '^' + expr # sane default

    r = gdb.execute('info types {}'.format(expr), False, True)
    #suspects
    for line in r.splitlines():
        log.debug('  %s', line)
        if line.startswith('File'):
            defsrc =  line.strip().lstrip('File').rstrip(':').strip()
            continue

        x = line.rstrip(';').split()
        if 'enum' not in x:
            continue

        i = x.index('enum')
        if len(x) < (i+1):
            log.debug('  ignoring line "{}"'.format(line))
            continue
        candidate = x[i] + ' ' + x[i+1]

        log.debug('Looking up candidate:%s', candidate)
        btype = getBasicType(candidate)
        log.debug('Basic type tag:%s, name: %s', btype.tag, btype.name)
        if not isEnumType(btype):
            continue

        name = btype.tag if btype.tag is not None else btype.name
        assert(name)
        if name in enumsd:
            log.debug('duplicate defs of "%s"', str(name))
            continue # TODO compare dups?
        members = gdb.types.make_enum_dict(btype)

        enumsd[name] = EnumInfo(members, expr, defsrc, name)

    return enumsd.values()

def main():
    args = envarg.getargs()

    logging.basicConfig(
        level=args.loglevel, #logging.DEBUG,
        stream=sys.stderr, #allow shell pipe of stdout if no outfile
        format='mkenumstr:%(levelname)s:%(name)s:%(lineno)04d: %(message)s')

    log.debug('-------- GDB --------')
    log.debug(str(args))
    #os.chdir(args.cwd)
    if not args.enum:
        log.error('No enum expr')
        return 0

    for infile in args.infile:
        if not os.path.isfile(infile):
            log.error('No such file "%s"', infile)
            return 1
        loadSymbols(infile)

    outd = []

    for expr in args.enum:

        enums = getEnums(expr)
        if not enums:
            log.warn('No enum(s) found from expression "%s"', expr)
            continue
        for enum in enums:
            d = enum.todict()
            outd.append(d)

    outs = json.dumps(outd, indent=4)
    if args.outfile is None:
        print(outs)
    else:
        with open(args.outfile, 'w') as fh:
            fh.write(outs)


    return 0


if __name__ == '__main__':
    main()
