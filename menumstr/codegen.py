import random
import string
import os

TABSTYLE = '  '
tabs = lambda n : n * TABSTYLE

def fileComments(kvcomments=None):
    c = [
    '/** AUTO GENERATED CODE BY MKENUMSTR */'
    ]
    return c

def includeDirectives(filelist, defundef=[]):
    c = []
    definelines = []
    undefineslines = []
    for k, v in defundef.items():
        definelines.append('#define {} {}'.format(k, v))
        undefineslines.append('#undef {}'.format(k))

    for inclfile in filelist:
        #log.debug(inclfile)
        include = '#include "{}"'.format(inclfile)
        if defundef:
            c.extend(definelines)
            c.append(include)
            c.extend(undefineslines)
        else:
            c.append(include)

    return c


def bitposMacroDefine(size):
    c = [
        tabs(1) + '/** Bit Mask Compare */',
        tabs(1) + '#define MSKCMP(X, POS) ((X) == (1u << POS)) ? POS :',
        tabs(1) + '/** single bit set or duplicate case value error */',
        tabs(1) + '#define BITPOS_INVALID_DEFAULT ({})'.format(size * 8),
        tabs(1) + '/** Better jumptable from cases */',
        tabs(1) + '#define BITPOS(X) (\\']

    fmt = tabs(2) + 'MSKCMP(X, {:>2}u) ' * 4 + '\\'

    for i in range(0, size * 8, 8):
        c.extend([
            fmt.format(i+0, i+1, i+2, i+3),
            fmt.format(i+4, i+5, i+6, i+7)
        ])

    c.extend([tabs(2) + 'BITPOS_INVALID_DEFAULT)', ''])

    return c

def bitposMacroCaseLbl(defname):
    return 'BITPOS({})'.format(defname)

def bitposMacroDefault():
    return 'BITPOS_INVALID_DEFAULT'

def bitposMacroUndef():
    c = [
        tabs(1) + '#undef MSKCMP',
        tabs(1) + '#undef BITPOS_INVALID_DEFAULT',
        tabs(1) + '#undef BITPOS']

    return c

def includeGuardBegin(fname):
    suffix='_INCLUDE_GUARD'
    if fname:
        basename = os.path.basename(fname).replace('.', '_').upper()
        defname = '{}{}'.format(basename, suffix)
    else:
        randchars = (random.choice(string.ascii_uppercase) for c in range(8))
        defname = 'UNKNOWN_OUTFILE_{}{}'.format(''.join(randchars), suffix)

    c = [
        '#ifndef {}'.format(defname),
        '#define {}'.format(defname),
        '']
    return c

def includeGuardEnd():
    return ['#endif /* END include guard */', ''] #extra lb at end of file

def funcParamName(usebitpos=False):
    return 'bitpos' if usebitpos else 'value'

def singlelineComment(comment, tablevel=0):
    return ['{}/*{}*/'.format(tabs(tablevel), comment)]

def funcDoxyComment(details={}, usebitpos=False, **kwargs):
    c = []
    prmname = funcParamName(usebitpos)

    if usebitpos:
        brief = 'Enum bit flag index to string lookup'
        param = 'bit position index representing a enum flag. (LSB == 0)'
    else:

        brief = 'Enum value to string lookup.'
        param = 'enum value.'
    c.extend([
        '/**',
        ' * @brief {}'.format(brief),
        ' * @note  Auto generated code.',
        ' * @param {} - {}'.format(prmname, param)
    ])

    if details:
        c.append(' * @details')
        for tag, comment in details.items():
            c.append(' *   {} {}'.format(tag, comment))
    c.append(' */')
    return c

def funcPrototype(funcname, funcprmtype, usebitpos=False, term='', **kwargs):
    prmname = funcParamName(usebitpos)
    prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                        func=funcname,
                        prmtype=funcprmtype,
                        prmname=prmname,
                        term=term)

    return [prototype]

def multilineComment(comments=[],tablevel=0, compact=True):
    #s = '{}/* '.format(tabs(tablevel))
    #for cm in comments:
    #    s += '{}* {}'.format(tabs(tablevel), cm))
    #commentlines = ['{}* {}'.format(tabs(tablevel), x) for x in comments]
    tabstr = tabs(tablevel)
    joinsep = '\n{} * '.format(tabstr)
    return ['{}/* {} */'.format(tabstr, joinsep.join(comments))]

def funcDefBegin(usebitpos=False, funcprmsize=4, **kwargs):
    prmname = funcParamName(usebitpos)
    c = ['{']
    if usebitpos:
        c.extend(bitposMacroDefine(funcprmsize))

    c.extend([
        '{}switch({})'.format(tabs(1), prmname),
        '{}{{'.format(tabs(1))# escpae '{' with '{{'
    ])
    return c

def funcDefCases(enumdefs, enumrepr, usedefs=True, usebitpos=False, **kwargs):
    c = []
    xindent = ''
    def caselblfmt(defname):
        label = defname if usedefs else int(enumdefs[defname])
        return bitposMacroCaseLbl(label) if usebitpos else label

    excluded = []
    for defname in sorted(enumdefs, key=enumdefs.get): # sort by value
        strname = enumrepr[defname]
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

def funcDefEnd(usebitpos=False, nameunknown='??', **kwargs):
    c = []
    if usebitpos:
        c.append('{}case {}:'.format(tabs(2), bitposMacroDefault()))

    c.extend([
        '{}default:'.format(tabs(2)),
        '{}return "{}";'.format(tabs(3), nameunknown),
        '{}}}'.format(tabs(1)) # escpae '}' with '}}'
    ])
    # ---- END switch case -----
    if usebitpos:
        c.extend(bitposMacroUndef())

    c.append('}')
    return c
