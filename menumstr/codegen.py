

def fileIncludeGuard(start, fname):
    suffix='_INCLUDE_GUARD'
    if fname:
        basename = os.path.basename(fname)
        defname = basename.replace('.', '_')
    else:
        defname = str(fname)

    defname = defname.upper() + suffix
    if start:
        src = [
            '#ifndef {}'.format(defname),
            '#define {}'.format(defname),
            '']
    else:
        src = ['#endif /* END include guard */', ''] #extra lb at end of file
    return src

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
                src.append(' *    {}: {}'.format(k, v)) #FIXME escape c '*/' etc
        src.append(' */')

    prototype = 'const char * {func}({prmtype} {prmname}){term}'.format(
                        func=funcname,
                        prmtype=funcprmtype,
                        prmname=prmname,
                        term=term)

    src.append(prototype)

    return src


def funcSourceBody(enumdefs, enumrepr, funcname, funcprmtype,
        usedefs=True, usebitpos=False, nameunknown='??', **kwargs):
    nameunknown = '??'
    tabstyle    = '  '
    xindent = ''
    prmname = funcParamName(usebitpos)
    '''
    src = funcPrototype(funcname, funcprmtype,
        usebitpos=usebitpos,
        prmname=prmname, term='\n{')
    '''
    src = []
    tabs = lambda n : n * tabstyle
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
        caselbl = defname if usedefs else int(enumdefs[defname])
        if usebitpos: caselbl = 'BITPOS32({})'.format(caselbl)

        src.extend([
            '{}case {}:'.format(tabs(2), caselbl),
            '{}return {}"{}";'.format(tabs(3), xindent, strname)
        ])

    for defname in excluded:
        caselbl = defname if usedefs else int(enumdefs[defname])
        src.extend([
            '{}case {}: /* excluded */'.format(tabs(2), caselbl)
        ])

    src.extend([
        '{}default:'.format(tabs(2)),
        '{}return "{}";'.format(tabs(2), nameunknown),
        '{}}}'.format(tabs(1)) # escpae '}' with '}}'
    ])
    # ---- END switch case -----
    src.append('}')
    return src
