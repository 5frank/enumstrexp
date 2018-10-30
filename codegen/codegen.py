import os
import re
TABSTYLE = '  '
tabs = lambda n : n * TABSTYLE


def fileDoxyComment(fname=None, kvcomments=None):
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
        '''
        Conforms to the standard practice and creates include
        guard macro named after the filename
        '''
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
    ''' Used internaly to create 'statistics' about generated
    lookup function. '''
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

        c = ['enum { // All strlen excl null term(s)',
            symbdef.format('MAXLEN', self.maxlen, ',', 'Longest string'),
            symbdef.format('TOTLEN', self.totlen, ',', 'All combined'),
            symbdef.format('STRCNT', self.strcnt, ' ', 'Number of strings'),
            '};',
        ]
        return c

class BitPosMacro(object):
    '''
    Generate Macros to covert a bit flag enum (example 1<<2) to bit index
    at compile time. Will generate different macros depending on
    bit flag size.
    Using bitpos macro makes generated code more transparent/readable as
    the original enums can be used instad of magic numbers.
    It also follows 'signgle point of truth'.
    '''
    def __init__(self, funcprmsize):
        '''
        @parameters:
            funcprmsize - str. the size of the function parameter '''
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

    def getUndefs(self):
        c = [
            tabs(1) + '#undef MSKCMP',
            tabs(1) + '#undef BITPOS_INVALID_DEFAULT',
            tabs(1) + '#undef BITPOS']
        return c

    def caseLabelFmt(self, defname):
        ''' wrap a enum name in the bitpos macro '''
        return 'BITPOS({})'.format(defname)

    def caseDefault(self):
        ''' the return value should be added togheter with the default
        case and will give a compiletime error on duplicate case value
        iff any enum have a invalid bit flag value. i.e. more then one bit
        set or zero
        '''
        return 'BITPOS_INVALID_DEFAULT'

class _Enums(object):
    '''
    Container of orginal enum definitions, values and their string
    representation to be used in generated code output
    '''
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

class EnumStrFunc(object):
    '''
    Generate a Enum to c-string lookup function.
    all code generator functions return list(s) containing valid  c-code
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
        '''
        init will only set up options. assumes enums to be added later.
        If some parameters are bad, and not checked for, it should give
        a error when trying to compile the generated c-code

        Parameters:
            funcname - symbol name on generated function
            funcprmtype -
            funcprmsize - int. must be a power of two
            usebitpos   - bool. use bit position/index as functin param
            usedefs - bool. use orignal enum definiton (not magic numbes)
            strstrip - regexp str. remove prefix etc from string name(s)
            stripcommonprefix - automagically remove common prefix
            exclude - regexpstr. exlude enum from generated lookup table
            doxydetails - details to be added in doxgen commet
            **kwargs - allows dict with unusd keys to be used as params
        '''
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
        self.nameunknown = '??'
        #self.opts = EnumStrFuncOpts(kwargs)
        self._enums = []
        #if usebitpos:
        if not self.funcprmname:
            self.funcprmname = 'bitpos' if usebitpos else 'value'
        self.bitposmacro = BitPosMacro(self.funcprmsize)

    def addEnums(self, enumdefs, defsrc='', name=''):
        '''
        Add/append enums for export.

        Parameters:
            enumdefs - dict. (<enum_name> : <int_value>,...}
            defsrc - str. file  where enum defined
            name - str. name of enum (only used in comments)
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
        '''
        Allows multiple calls, will only add cases.
        Parameters:
            enumdefs - dict. {<enum_def_name> : <value>, ...}
            enumrepr - dict. {<enum_def_name> : <string_repr>, ...}
        '''
        c = []

        xindent = ''
        def caseLabelFmt(defname):
            label = defname if self.usedefs else int(enumdefs[defname])
            if self.usebitpos:
                label = self.bitposmacro.caseLabelFmt(label)
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
                '{}case {}:'.format(tabs(2), caseLabelFmt(defname)),
                '{}return {}"{}";'.format(tabs(3), xindent, strname)
            ])

        for defname in excluded:
            c.extend([
            '{}/* case {}:  excluded */'.format(tabs(2), caseLabelFmt(defname))
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
        ''' Get generated code '''
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
