import os
import re
TABSTYLE = '  '
tabs = lambda n : n * TABSTYLE


def doxyFileComments(fname=None, kvcomments=None):
    c = ['/**']
    if fname:
        basename = os.path.basename(fname)
        c.append(' * @file {}'.format(os.path.basename(fname)))
    c.extend([
        ' * @brief Auto generated code by mkenumstr',
        ' * @note Take care not modify this file in case it is generated',
        ' *    by a build script as edits might be overwritten',
        ' */'
    ])
    return c

def includeDirectives(filelist, defundef={}):
    c = []
    if defundef:
        definelines = []
        undefineslines = []
        for k, v in defundef.items():
            definelines.append('#define {} {}'.format(k, v))
            undefineslines.append('#undef {}'.format(k))

        for inclfile in filelist:
            include = '#include "{}"'.format(inclfile)
            c.extend(definelines)
            c.append(include)
            c.extend(undefineslines)
    else:
        c = ['#include "{}"'.format(hf) for hf in filelist]

    return c

class IncludeGuard(object):

    def __init__(self, fname, suffix='_INCLUDE_H_'):
        if fname:
            basename = os.path.basename(fname).split('.')[0].upper()
        else:
            basename = 'UNKNOWN_OUTFILE'
        self.defname = '{}{}'.format(basename, suffix)

    def guardBegin(self):
        return [
            '#ifndef {}'.format(self.defname),
            '#define {}'.format(self.defname),
            ''
        ]

    def guardEnd(self):
        #will alos add extra lb at end of file
        return ['#endif /*END: {} */'.format(self.defname), '']


class _EnumStrFuncStats(object):
    def __init__(self, funcname):
        self.funcname = funcname
        self.maxlen = 0
        self.totlen = 0
        self.strcnt = 0

    def update(self, enumrepr):
        ''' enumrepr '''
        for em in enumrepr:
            if enumrepr[em] is None: continue
            strlen = len(enumrepr[em])
            self.maxlen = max(self.maxlen, strlen)
            self.totlen += strlen
            self.strcnt += 1

    def getMacros(self):
        def comment(text):
            return '/** {} */'.format(text)
        def ppdefine(suffix, value):
            return '#define {}_{} ({})'.format(self.funcname, suffix, value)

        c = [
            comment('Length of the longest string. (excl null term)'),
            ppdefine('MAXLEN', self.maxlen),
            comment('Total length of all strings combined (excl null term)'),
            ppdefine('TOTLEN', self.totlen),
            comment('String count - number of strings in the lookup table'),
            ppdefine('STRCNT', self.strcnt)
        ]
        return c

    def getEnums(self):
        comment = '/* {} */'
        symbdef = tabs(1) + self.funcname + '_{} = {:>4}{} //!< {}'

        c = [
        #'enum {}_e{ '.format(self.funcname),

        'enum { // All strlen excl null term(s)',
        symbdef.format('MAXLEN', self.maxlen, ',', 'Longest string'),
        symbdef.format('TOTLEN', self.totlen, ',', 'All combined'),
        symbdef.format('STRCNT', self.strcnt, ' ', 'Number of strings'),
        '};',]
        return c

class BitPosMacro(object):
    def __init__(self, funcprmsize):
        ''' @param size - the size of the function parameter '''
        self.numbits = funcprmsize * 8 #almost alwyas 8 bits per char

    def getDefines(self):
        c = [
            tabs(1) + '/** Bit Mask Compare */',
            tabs(1) + '#define MSKCMP(X, POS) ((X) == (1u << POS)) ? POS :',
            tabs(1) + '/** single bit set or duplicate case value error */',
            tabs(1) + '#define BITPOS_INVALID_DEFAULT ({})'.format(self.numbits),
            tabs(1) + '/** Better jumptable from cases */',
            tabs(1) + '#define BITPOS(X) (\\']

        fmt = tabs(2) + 'MSKCMP(X, {:>2}u) ' * 4 + '\\'

        for i in range(0, self.numbits, 8):
            c.extend([
                fmt.format(i+0, i+1, i+2, i+3),
                fmt.format(i+4, i+5, i+6, i+7)
            ])

        c.extend([tabs(2) + 'BITPOS_INVALID_DEFAULT)', ''])

        return c

    def getUndefs():
        c = [
            tabs(1) + '#undef MSKCMP',
            tabs(1) + '#undef BITPOS_INVALID_DEFAULT',
            tabs(1) + '#undef BITPOS']
        return c

    def caseLblFmt(defname):
        return 'BITPOS({})'.format(defname)

    def caseDefault():
        return 'BITPOS_INVALID_DEFAULT'

class _Enums(object):
    ''' Continer of orginal enum definitions, values and string representation
    to be used in generated code '''
    def __init__(self, enumdefs, defsrc='', name=''):
        self.enumdefs = enumdefs # {<enum_def_name> : <value>, ...}
        #self.enumrepr = enumrepr # {<enum_def_name> : <string_repr>, ...}
        self.defsrc = defsrc
        self.name = name

    def getComment(self, tablvl=0):
        defsrc = os.path.basename(self.defsrc) if self.defsrc else ''
        enMinVal = min(self.enumdefs.values())
        enMaxVal = max(self.enumdefs.values())
        comments = [
            '{}/* defsrc:{}'.format(tabs(tablvl), defsrc),
            '{} * enum: {} min: {} max: {} */ '.format(
            tabs(tablvl), self.name, enMinVal, enMaxVal)
        ]
        return comments


'''
class EnumStrFuncOpts(object):
    def __init__(self, **kwargs):
        # TODO sanity check and happy linter

        self.funcprmname = funcprmname
        self.funcprmtype = funcprmtype
        self.funcprmsize = funcprmsize
        self.funcname = funcname
        self.usebitpos = usebitpos
        #for k, v i kwargs.items():

        self.__dict__.update(kwargs)
                if not self.funcprmname:
                    self.funcprmname = 'bitpos' if self.usebitpos else 'value'

    def __iter__(self):
        for k,v in self.__dict__.items():
            yield k,v

    def __str__(self):
        return str(self.__dict__)
'''

class EnumStrFunc(object):
    ''' Generate a Enum to c-string lookup function.
    all code generator functions return list(s) of containing lines of code
    or comments.
    '''
    def __init__(self,
                funcname,
                funcprmtype,
                funcprmsize=4,
                funcprmname=None,
                usebitpos=False,
                usedefs=True,
                strstrip=None,
                stripcommonprefix=False,
                exclude=None,
                doxydetails=[],
                **kwargs):

        self.funcprmname = funcprmname
        self.funcprmtype = funcprmtype
        self.funcprmsize = funcprmsize
        self.funcname = funcname
        self.usebitpos = usebitpos
        self.usedefs = usedefs
        self.strstrip = strstrip
        self.stripcommonprefix = stripcommonprefix
        self.exclude = exclude
        self.doxydetails = doxydetails
        self.nameunknown='??'
        #self.opts = EnumStrFuncOpts(kwargs)
        self._enums = []
        #if usebitpos:
        if not self.funcprmname:
            self.funcprmname = 'bitpos' if usebitpos else 'value'
        self.bitposmacro = BitPosMacro(self.funcprmsize)

    def addEnums(self, enumdefs, defsrc='', name=''):
        ''' add/append enums for export.
        @param enumdefs must be dict with (<enum_name> : <int_value>,...}
        '''
        #enumrepr = self.createEnumRepr(enumdefs)
        self._enums.append(_Enums(enumdefs, defsrc, name))

    def createEnumRepr(self, emnumdefs):
        #log.debug(emnumdefs)
        if self.strstrip is not None: # none if self.strstrip == ''
            restrip = re.compile(self.strstrip)
            stripper = lambda x : restrip.sub('', x)

        elif self.stripcommonprefix:
            prefix = os.path.commonprefix(emnumdefs.keys())
            restrip = re.compile('^{}'.format(prefix))
            stripper = lambda x : restrip.sub('', x)

        else:
            stripper = lambda x : x

        if self.exclude:
            reexcl = re.compile(self.exclude)
            excluder = lambda x : reexcl.search(x) is not None
        else:
            excluder = lambda x : False

        enumrepr = {}
        for name, val in emnumdefs.items():
            enumrepr[name] = None if excluder(name) else stripper(name)

        return enumrepr

    def funcDoxyComment(self):
        c = []

        if self.usebitpos:
            briefdoc = 'Enum bit flag index to string lookup'
            paramdoc = 'bit position index representing a enum flag. (LSB == 0)'
        else:
            briefdoc = 'Enum value to string lookup.'
            paramdoc = 'enum value.'

        c.extend([
            '/**',
            ' * @brief Generated code by mkenumstr. {}'.format(briefdoc),
            ' * @param {} - {}'.format(self.funcprmname, paramdoc)
        ])

        if self.doxydetails:
            c.append(' * @details')
            for line in self.doxydetails:
                c.append(' *   {}'.format(line))
        c.append(' */')
        return c

    def funcPrototype(self, term):
        prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                            func=self.funcname,
                            prmtype=self.funcprmtype,
                            prmname=self.funcprmname,
                            term=term)

        return [prototype]

    def funcDefBegin(self):

        c = ['{']
        if self.usebitpos:
            c.extend(self.bitposmacro.getDefines())

        c.extend([
            '{}switch({})'.format(tabs(1), self.funcprmname),
            '{}{{'.format(tabs(1))# escpae '{' with '{{'
        ])

        return c

    def funcDefCases(self, enumdefs, enumrepr):
        c = []

        xindent = ''
        def caselblfmt(defname):
            label = defname if self.usedefs else int(enumdefs[defname])
            if self.usebitpos:
                label = self.bitposmacro.caseLblFmt(label)
            return label

        excluded = []
        for defname in sorted(enumdefs, key=enumdefs.get): # sort by value
            strname = enumrepr[defname]
            if self.usebitpos and int(enumdefs[defname]) == 0:
                excluded.append(defname)
                continue
            if strname is None:
                excluded.append(defname)
                continue
            c.extend([
                '{}case {}:'.format(tabs(2), caselblfmt(defname)),
                '{}return {}"{}";'.format(tabs(3), xindent, strname)
            ])

        for defname in excluded:
            c.extend([
            '{}/* case {}:  excluded */'.format(tabs(2), caselblfmt(defname))
            ])

        return c


    def funcDefEnd(self):
        c = []
        if self.usebitpos:
            label = self.bitposmacro.caseDefault()
            c.append('{}case {}:'.format(tabs(2), label))

        c.extend([
            '{}default:'.format(tabs(2)),
            '{}return "{}";'.format(tabs(3), self.nameunknown),
            '{}}}'.format(tabs(1)) # escpae '}' with '}}'
        ])
        # ---- END switch case -----
        if self.usebitpos:
            c.extend(self.bitposmacro.getUndefs())

        c.append('}')
        return c

    def generate(self):
        c = []
        h = []

        if len(self._enums) > 1:
            self._enums.sort(key=lambda en: min(en.enumdefs.values()))
        doxycomments = self.funcDoxyComment()
        c.extend(doxycomments)
        c.extend(self.funcPrototype(term=''))
        c.extend(self.funcDefBegin())
        funcstats = _EnumStrFuncStats(self.funcname)
        for en in self._enums:
            enumrepr = self.createEnumRepr(en.enumdefs)
            funcstats.update(enumrepr)
            c.extend(en.getComment(tablvl=2))
            c.extend(self.funcDefCases(en.enumdefs, enumrepr))

        c.extend(self.funcDefEnd())

        h.extend(doxycomments)
        h.extend(funcstats.getEnums())
        h.extend(self.funcPrototype(term=';'))
        h.append('') #new line

        return c, h
