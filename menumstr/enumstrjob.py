'''

'''
#import shlex
import re
import logging
log = logging.getLogger(__file__)


class BadExprException(Exception):
    def __init__(self, msg=''):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return '{}()'.format(self.__class__.__name__, self.msg)


def isCStr(s):
    return s.startswith('"') and s.endswith('"')

def stripCStr(s):
    return s[1:-1]

def stripAssumedCStr(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    else:
        raise BadExprException('refmt assumed c string')


class CCodeGen(object):
    def __init__(self, job):
        self.__job = job

    def genSwitchCase(self, prmname='x', tablvl=1, default='<?>'):
        job = self.__job
        if not job.enumdefs:
            return default #FIXME
        assert (job.enumrepr)

        reprvkd = job.enumrepr
        defsvkd = {v: k for k, v in job.enumdefs.iteritems()}

        asbitflags = job.asbitflags
        usedefs = job.usedefs
        tabs = lambda n : n * '  ' #TODO from config

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

    def genFunc(self):
        job = self.__job
        if job.asbitflags:
            prmname = 'bitpos'
            brief = 'Enum bit flag index to string lookup'
            param = 'bit position index representing a enum flag. (LSB == 0)'
        else:
            prmname = 'value'
            brief = 'Enum value to string lookup.'
            param = 'enum value.'

        s =  '/**\n'
        s += ' * @brief {}\n'.format(brief)
        s += ' * @note  Do not modify! Auto generated code.\n'
        s += ' * @param {} - {}\n'.format(prmname, param)
        for k, v in job.meta.items():
            if v:
                s += ' *    {}: {}\n'.format(k, v) #FIXME escape c '*/' etc
        s += ' */\n'

        m = job.meta
        s += '{} {}({} {})\n'.format(
                m['funcrettype'], m['funcname'], m['funcprmtype'], prmname)
        s += '{\n'
        s += self.genSwitchCase(prmname=prmname)
        s += '}\n'
        return s

    def get(self):
        return self.genFunc()

    def export(self, fh):
        raise KeyError #TODO


class EnumStrReformat(object):
    def __init__(self):
        self._fmtseq = []

    def docstr(self):
        return [str(f[0].__name__) + str(tuple(f[1])) for f in self._fmtseq]

    def addFmt(self, func, prms=[]):
        self._fmtseq.append((func, prms))

    def applyFmt(self, enums):
        for fmt in self._fmtseq:
            fmtfunc = fmt[0]
            fmtargs = fmt[1]
            assert(callable(fmtfunc))
            enums = fmtfunc(enums, *fmtargs)
        return enums

    def findcommonxfix(self, x, enums, maxunmatch=1, minlen=2):
        if x == 'pre':
            return self.findCommonPrefix(enums, maxunmatch, minlen)
        elif x == 'suf':
            return self.findCommonSuffix(enums, maxunmatch, minlen)
        else:
            raise KeyError

    def findCommonPrefix(self, enums, maxunmatch=1, minlen=2):
        '''Given a list of strings, returns the longest common string,
        ignoring max N unmatched strings set by param, or empty string
        '''
        members = enums.keys()
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
            if ignored <= maxunmatch:
                commons[i] = max(d, key=d.get) # add winner
            else:
                break
        res = ''.join(commons)
        if len(res) < minlen:
            res = ''
        return res

    def replace(self, enums, findexpr, replacewith=''):
        reobj = re.compile(findexpr)
        r = {reobj.sub(replacewith, k): v for (k, v) in enums.iteritems()}
        assert(len(r) == len(enums)) # conflicting keys
        return r


class EnumStrJob(object):
    def __init__(self, toks=[], meta={}, asbitflags=False):
        #self._refmtfuncs = []
        self.refmt = EnumStrReformat()
        self.codegen = CCodeGen(self)
        self.asbitflags = asbitflags
        self.meta = meta
        self.fromtype = None
        self.usedefs = True #TOTO
        self.toks = toks
        self.enumdefs = {}
        self.enumrepr = {}

        self._parsers = {
            'fromtype' :   self.parse_fromtype,
            'reformat' :   self.parse_reformat,
            'sansprefix' : self.parse_sansprefix,
            'sanssuffix' : self.parse_sanssuffix,
        }
        #need type argument know, format args parsed later when we have the enum
        self.parse(self.toks, selfunc='fromtype')

        if not self.fromtype:
            self.fromtype = meta['funcprmtype']

    def __str__(self):
        return str(self.toks)

    def renderCode(self):
        if not self.enumdefs:
            log.error("no defs")
            #raise KeyError # FIXME log.warning('No defs for {}'.format(job))
            return
        self.parse(self.toks)
        self._prepareRepr()
        return self.codegen.get()

    def _prepareRepr(self):
        #alter repr as specified
        tmpd = self.refmt.applyFmt(self.enumdefs)
        # from <name>:<val> to <val>:<name> and merge duplicats
        self.enumrepr = {} #clear
        duplsep = '=='
        duplicates = 0
        for name, val in tmpd.items():
            val = int(val)
            if val in self.enumrepr:
                 self.enumrepr[val] += duplsep + name
                 duplicates += 1
            else:
                self.enumrepr[val] = name
        self.meta['duplicates'] = duplicates


    def parse_fromtype(self, args):
        if len(args) != 1:
            msg = ' accepts 1 arguments but {} given'.format(len(args))
            raise BadExprException(msg)
        atype = args[0]
        if isCStr(atype):
            atype = stripCStr(atype)
            self.fromtypeexposed = False
        else:
            self.fromtypeexposed = True
        self.fromtype = atype

    def parse_reformat(self, args):
        if len(args) != 2:
            msg = 'reformat accepts 2 arguments but {} given'.format(len(args))
            raise BadExprException(msg)
        prms = []
        for arg in args:
            if not isCStr(arg):
                raise BadExprException('reformat args must be a strings')
            prms.append(stripCStr(arg))
        self.refmt.addFmt(self.refmt.replace, prms)

    def _parse_sansxfix(self, x, args):
        if x == 'pre':
            refindfmt = '^{}'
        elif x == 'suf':
            refindfmt = '{}$'
        else:
            raise KeyError

        if len(args) == 0 or args[0] == 'COMMON':
            findprms = []
            if len(args) > 2:
                try:
                    findprms = [int(a) for a in args[1:]]
                except ValueError as e:
                    raise BadExprException(str(e))

            xfix = self.refmt.findcommonxfix(x, self.enumdefs, *findprms)
            self.meta['common_{}fix_found'.format(x)] = xfix
            if not xfix:
                log.warning('No %sfix found', xfix)
                return
            prms = [refindfmt.format(xfix), '']
            self.refmt.addFmt(self.refmt.replace, prms)

        else:
            for arg in args:
                if not isCStr(arg):
                    raise BadExprException()
                prms = [refindfmt.format(stripCStr(arg)), '']
                self.refmt.addFmt(self.refmt.replace, prms)

    def parse_sansprefix(self, args):
        return self._parse_sansxfix('pre', args)

    def parse_sanssuffix(self, args):
        return self._parse_sansxfix('suf', args)

    def parse(self, toks, selfunc=None):
        for tok in toks:
            if len(tok) == 0:
                continue
            self.parsetok(tok, selfunc)

    def parsetok(self, tok, selfunc=None):
        if selfunc is not None:
            assert(selfunc in self._parsers)

        m = re.search(r'(.*?)\((.*?)\)', str(tok))
        if not m:
            msg = 'Failed to parse "{}"'.format(tok)
            raise BadExprException(msg)
        func = m.group(1)
        args = m.group(2).split(',')
        #args = [a.strip() for a in args]
        args = map(lambda a: a.strip(), args)
        args = filter(len, args) #remove empty

        if func in self._parsers:
            if selfunc is None or selfunc == func:
                log.debug('parsing %s', func)
                self._parsers[func](args)
        else:
            msg = 'unknown keyword or function "{}"'.format(tok)
            raise BadExprException(msg)


import unittest
from pprint import pprint
def main():
    toks = ['reformat("c", "keso")', 'sansprefix()', 'fromtype(x_t)']
    opts = EnumStrJob(toks)
    print(opts)
    pprint(opts.refmt.docstr())


if __name__ == '__main__':
    main()
