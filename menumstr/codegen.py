import random
import string

TABSTYLE = '  '
tabs = lambda n : n * TABSTYLE

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
            srclines.extend(include)
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

def funcPrototype(funcname, funcprmtype,
                prmname=None,
                kvcomments={},
                usebitpos=False, withcomments=True, term='', **kwargs):

    if prmname is None:
        prmname = funcParamName(usebitpos)

    src = []
    if usebitpos:
        brief = 'Enum bit flag index to string lookup'
        param = 'bit position index representing a enum flag. (LSB == 0)'
    else:

        brief = 'Enum value to string lookup.'
        param = 'enum value.'

    if withcomments:
        src.extend([
            '/**',
            ' * @brief {}'.format(brief),
            ' * @note  Do not modify! Auto generated code.',
            ' * @param {} - {}'.format(prmname, param)
        ])
        for k, v in kvcomments.items():
            if v:
                #TODO escape c '*/' etc
                #sk = k.replace.('*/',
                src.append(' *    {}: {}'.format(k, v))

        src.append(' */')

    prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                        func=funcname,
                        prmtype=funcprmtype,
                        prmname=prmname,
                        term=term)

    src.append(prototype)

    return src


def funcSourceBody(enumdefs, enumrepr, funcname, funcprmtype,
        usedefs=True, usebitpos=False, funcprmsize=4,
        nameunknown='\\?\\?', **kwargs):
    xindent = ''
    prmname = funcParamName(usebitpos)
    src = []
    if usebitpos:
        src.extend(bitposMacroDefine(funcprmsize))

    def caselblfmt(defname):
        r = defname if usedefs else int(enumdefs[defname])
        if usebitpos:
            return bitposMacroCaseLbl(defname)
        else:
            return r

    src.extend([
        '{}switch({})'.format(tabs(1), prmname),
        '{}{{'.format(tabs(1))# escpae '{' with '{{'
    ])

    excluded = []
    for defname in sorted(enumdefs, key=enumdefs.get): # sor by value
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
            '{}case {}: /* excluded */'.format(tabs(2), caselblfmt(defname))
        ])

    if usebitpos:
        src.append('{}case {}:'.format(tabs(2), bitposMacroDefault()))

    src.extend([
        '{}default:'.format(tabs(2)),
        '{}return "{}";'.format(tabs(2), nameunknown),
        '{}}}'.format(tabs(1)) # escpae '}' with '}}'
    ])
    # ---- END switch case -----
    if usebitpos:
        src.extend(bitposMacroUndef())

    src.append('}')
    return src
