import random
import string
import os

TABSTYLE = '  '
tabs = lambda n : n * TABSTYLE

def fileComments(kvcomments=None):
    srclines = [
    '/** AUTO GENERATED CODE BY MKENUMSTR */'
    ]
    return srclines

def includeDirectives(filelist, defundef=[]):
    definelines = []
    undefineslines = []
    for duw in defundef:
        definelines.append('#define {}'.format(duw))
        undefineslines.append('#undef {}'.format(duw))

    srclines = []

    for inclfile in filelist:
        #log.debug(inclfile)
        include = '#include "{}"'.format(inclfile)
        if defundef:
            srclines.extend(definelines)
            srclines.append(include)
            srclines.extend(undefineslines)
        else:
            srclines.append(include)

    return srclines


def bitposMacroDefine(size):
    srclines = [
        tabs(1) + '/** Bit Mask Compare */',
        tabs(1) + '#define MSKCMP(X, POS) ((X) == (1u << POS)) ? POS :',
        tabs(1) + '/** single bit set or duplicate case value error */',
        tabs(1) + '#define BITPOS_INVALID_DEFAULT ({})'.format(size * 8),
        tabs(1) + '/** Better jumptable from cases */',
        tabs(1) + '#define BITPOS(X) (\\']

    fmt = tabs(2) + 'MSKCMP(X, {0:>2}u) ' * 4 + '\\'

    for i in range(0, size * 8, 8):
        srclines.extend([
            fmt.format(i+0, i+1, i+2, i+3),
            fmt.format(i+4, i+5, i+6, i+7)
        ])

    srclines.extend([tabs(2) + 'BITPOS_INVALID_DEFAULT)', ''])

    return srclines

def bitposMacroCaseLbl(defname):
    return 'BITPOS({})'.format(defname)

def bitposMacroDefault():
    return 'BITPOS_INVALID_DEFAULT'

def bitposMacroUndef():
    srclines = [
        tabs(1) + '#undef MSKCMP',
        tabs(1) + '#undef BITPOS_INVALID_DEFAULT',
        tabs(1) + '#undef BITPOS']

    return srclines


def includeGuardBegin(fname):
    suffix='_INCLUDE_GUARD'
    if fname:
        basename = os.path.basename(fname).replace('.', '_').upper()
        defname = '{}{}'.format(basename, suffix)
    else:
        randchars = (random.choice(string.ascii_uppercase) for c in range(8))
        defname = 'UNKNOWN_OUTFILE_{}{}'.format(''.join(randchars), suffix)

    src = [
        '#ifndef {}'.format(defname),
        '#define {}'.format(defname),
        '']
    return src

def includeGuardEnd():
    return ['#endif /* END include guard */', ''] #extra lb at end of file

def funcParamName(usebitpos=False):
    return 'bitpos' if usebitpos else 'value'

def funcPrototype(funcname, funcprmtype, usebitpos=False, term='', **kwargs):
    prmname = funcParamName(usebitpos)
    prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                        func=funcname,
                        prmtype=funcprmtype,
                        prmname=prmname,
                        term=term)

    return [prototype]


def singlelineComment(comment, tablevel=0):
    return ['{}/*{}*/'.format(tabs(tablevel), comment)]

def funcDoxyComment(details={}, usebitpos=False, **kwargs):
    src = []
    prmname = funcParamName(usebitpos)

    if usebitpos:
        brief = 'Enum bit flag index to string lookup'
        param = 'bit position index representing a enum flag. (LSB == 0)'
    else:

        brief = 'Enum value to string lookup.'
        param = 'enum value.'
    src.extend([
        '/**',
        ' * @brief {}'.format(brief),
        ' * @note  Auto generated code.',
        ' * @param {} - {}'.format(prmname, param)
    ])

    if details:
        src.append(' * @details')
        for tag, comment in details.items():
            src.append(' *   {} {}'.format(tag, comment))
    src.append(' */')
    return src


def multilineComment(comments=[],tablevel=0, compact=True):
    #s = '{}/* '.format(tabs(tablevel))
    #for cm in comments:
    #    s += '{}* {}'.format(tabs(tablevel), cm))
    #commentlines = ['{}* {}'.format(tabs(tablevel), x) for x in comments]
    tabstr = tabs(tablevel)
    joinsep = '\n{} * '.format(tabstr)
    return ['{}/* {} */'.format(tabstr, joinsep.join(comments))]
    #return src

def funcDefBegin(usebitpos=False, funcprmsize=4, **kwargs):
    prmname = funcParamName(usebitpos)
    src = ['{']
    if usebitpos:
        src.extend(bitposMacroDefine(funcprmsize))

    src.extend([
        '{}switch({})'.format(tabs(1), prmname),
        '{}{{'.format(tabs(1))# escpae '{' with '{{'
    ])
    return src


def funcDefCases(enumdefs, enumrepr, usedefs=True, usebitpos=False, **kwargs):
    src = []
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
        src.extend([
            '{}case {}:'.format(tabs(2), caselblfmt(defname)),
            '{}return {}"{}";'.format(tabs(3), xindent, strname)
        ])

    for defname in excluded:
        src.extend([
            '{}/* case {}:  excluded */'.format(tabs(2), caselblfmt(defname))
        ])

    return src

def funcDefEnd(usebitpos=False, nameunknown='??', **kwargs):
    src = []
    if usebitpos:
        src.append('{}case {}:'.format(tabs(2), bitposMacroDefault()))

    src.extend([
        '{}default:'.format(tabs(2)),
        '{}return "{}";'.format(tabs(3), nameunknown),
        '{}}}'.format(tabs(1)) # escpae '}' with '}}'
    ])
    # ---- END switch case -----
    if usebitpos:
        src.extend(bitposMacroUndef())

    src.append('}')
    return src
