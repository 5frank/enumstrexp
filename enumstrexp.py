''' require gdb > 7.3 ? '''
import gdb
import gdb.types
import re
from os.path import basename
from operator import attrgetter

'''  
DOC
embedded...

TODO 
- handle empty strings after strip
- input source elf or directory (auto)
- flags or enum 0,1,2... (auto?)
  - if flag, utput max alloc size
- smart/guess strip common if N>5 && N-2 is equal. N = nr of enum instances
- output options:

    flags
        macro header only x&a? a: x&b? b:....
    iter nr
        macro header only x==a? a: x==b? b:....
        cswitch
        clUt
        pydict
- add detailed comments on parser result
- include doxygen comments. is lib?


ENUMASSTR(typedefName, value)

class Opts():
    opFmts = ['cswitch', 'cmacro', 'clut']
    def __init__(self, defaults=None):
        self.name = ""
        self.doxygenIncl = False
        self.opFmt = Opts.opFmts[0]
        self.srcFile = ""
        self.protype = ""

defaultOpt = Opts():
'''
def missingCntGaps(ed, maxGaps=512):
    edMax = ed[max(ed, key=ed.get)]
    if edMax-len(ed) > maxGaps: return None
    vd = {} # valud dict
    for k in ed:
        vd[ed[k]] = k
    missing = []
    x0 = 0
    x1find = False
    
    for i in range(0,edMax):
        if not i in vd and not x1find:
            x0 = i
            x1find = True
        elif x1find: # and v in vd
            x1 = i
            missing.append( (x0,x1) )
    return missing

def minValMember(ed):
    return min(ed, key=ed.get)

def maxValMember(ed):
    return max(ed, key=ed.get)

class fmt():
    pre = 'ENUMSTREXP_'
    tab = '  '
    eol = '\n'
    linemax = 80 # TODO
    #macroEOL = '\\\n'
    def cstr(x):
        return '\"' + str(x) + '\"'
    def tabs(n):
        return n * fmt.tab
#fmt = Format()


class EnumBaseClass():
    def __init__(self, enumId, exportId = True, stripPrefix = True):
        isAnonymous = False
        self.enumId = enumId
        self.gdbType = self._init_gdbType(enumId)
        self.enumMap = self._init_enumMap(self.gdbType)
        self.definedInFile  = self._init_definedInFile(enumId)
        self.stripPrefix = None
        self.symToStrFilt  = self._init_symToStrFilt(stripPrefix)
        self.exportId = self._init_exportId(enumId, exportId)
        self.valMaxStrLen = 0
        self.symMaxStrLen = 0
        self.valMap = {}
        # init other dicts etc from enum
        for enumSym in self.enumMap:
            symStr = str(enumSym)
            val = int(self.enumMap[enumSym])
            self.valMap[val] = symStr
            symLen = len(self.symToStrFilt(symStr))
            if symLen > self.symMaxStrLen: self.symMaxStrLen = symLen
            valLen = len(str(val))
            if valLen > self.valMaxStrLen: self.valMaxStrLen = valLen

    # Find enum type and get enum dict
    def _init_gdbType(self, enumId):
        t = None
        #TODO from gdb type...
        def isEnum(t):            
            if t == None: return False
            ts = t.strip_typedefs()
            if ts.code == gdb.TYPE_CODE_ENUM: return True
            return False
        # Type from enum typedef id
        # def tFromTypedef(sid):
        try:    
            t = gdb.types.get_basic_type(gdb.lookup_type(enumId))
            if not isEnum(t):
                raise LookupError('\'' + enumId + '\' is not a enum')
        except RuntimeError:
            # Try find type from enum member name
            try: 
                t = gdb.parse_and_eval(enumId).type
                if not isEnum(t): 
                    raise LookupError('\'' + enumId + '\' is not a enum')
            except RuntimeError: 
                raise LookupError('No enum found from \''+enumId+'\'')
        # success, enum instance found
        return t

    # Find enum type and get enum dict
    def _init_enumMap(self, etype):
        # success, enum instance found, get dict
        bt = gdb.types.get_basic_type(etype)
        enumDict =  gdb.types.make_enum_dict(bt)
        return enumDict

    # init name strip modifier
    def _init_symToStrFilt(self, stripPrefix):
        # Return empty string if no common found
        def findCommonPrefix(enumMap):
            pfix = '';
            lened = len(enumMap)
            if lened <= 1: return ''
            elif lened == 2: maxNotMatch = 1
            else: maxNotMatch = 2
            def nthChrTopCandidate(n, d):
                dr = {}
                for k in d:
                    s = str(k)
                    if n >= len(s): return None
                    c = s[n]
                    if c in dr: dr[c] += 1
                    else: dr[c] = 1
                if len(dr) >= maxNotMatch: return None
                return max(dr)
            i = 0;
            while 1:
                c = nthChrTopCandidate(i, enumMap)
                if c == None: return pfix
                else: pfix += c
                i += 1
        if isinstance(stripPrefix, str) and stripPrefix != '':
            self.stripPrefix = stripPrefix
            return lambda nm : str(nm).lstrip(stripPrefix)
        elif stripPrefix == True:
            #if self.enumMap =) {}: return
            stripStr = findCommonPrefix(self.enumMap)
            self.stripPrefix = stripStr
            return lambda nm: str(nm).lstrip(stripStr)
        else:
            self.stripPrefix = ''
            return lambda nm : str(nm) #default

    def _init_exportId(self, enumId, exportId):
        exportIdStr = ''
        # auto set from enumId
        if exportId == True: exportIdStr = enumId
        # Verify a valid name space
        research = re.compile(r'[^a-zA-Z0-9_]').search
        if bool(research(exportIdStr)) or len(exportIdStr) < 1:
            raise LookupError('\'' + self.exportId + '\' is not a valid name space string')
        return exportIdStr
    
    # @return the file enum defined in
    def _init_definedInFile(self, symbName):
        r = gdb.execute('info types ^'+symbName +'$', False, True)
        for l in r.splitlines():
            if l.startswith('File'):
                return l.strip().lstrip('File').rstrip(":")
        return None

    def _fmt_c_baseComment(self):
        s = ''
        s += ' * Autogenerated code by enumstrexp.py.\n'
        s += ' * Enum defined in file: ' + self.definedInFile + '\n' 
        s += ' * Enum identifier: ' + self.enumId + '\n' 
        s += ' * Enum prefix stripped: \'' + self.stripPrefix + '\' \n' 
        return s

class EnumContCount(EnumBaseClass):
    def __init__(self, enumId, exportId = True, stripPrefix = True):
        super(EnumContCount, self).__init__(enumId, exportId, stripPrefix)
        self.valSorted = sorted(self.valMap) # value sorted list

    def _fmt_c_ternary(self, exportId = ''):
        s = ''
        s += '/**\n' 
        s += self._fmt_c_baseComment()
        s += ' *\n'
        s += ' * Translater: \n'
        s += ' * @param  v [in] a int value derived from \n'
        s += ' *         enum ' + self.enumId +'\n'
        s += ' * @return A c string representing the enum or default unknown if \n'
        s += ' *         no value found.\n'
        s += ' */\n'
        s += '#define ' + fmt.pre + 'TRANSLATE__'+self.exportId+'(v) (\\\n'
        for val in self.valSorted:
            valStr = str(val)
            symStr = self.symToStrFilt(self.valMap[val])
            indents = ' '*(self.valMaxStrLen - len(valStr))
            s += fmt.tabs(1) + '(v == ' + indents + valStr + ') ? ' 
            s += fmt.cstr(symStr) + ':\\\n'
        s += '  \"Unknown_'+self.exportId+'\" ) /*Default*/\n'
        return s

    # tabLvl - add extra indents in output 
    def _fmt_c_switch(self, tabLvl = 0, eolAfterCaseStatement = False):
        s = ''
        n = tabLvl # tab level
        s += fmt.tabs(n) + 'switch(v)\n' 
        s += fmt.tabs(n) +'\n{\n'
        n += 1
        for val in self.valSorted:
            valStr = str(val)
            symStr = self.symToStrFilt(self.valMap[val])
            if eolAfterCaseStatement:
                s += fmt.tabs(n) + 'case ' + valStr + ':\n'
                s += fmt.tabs(n+1) + 'return \"' + symStr + '\";\n'
            else:
                indents = ' '*(self.valMaxStrLen - len(valStr)) 
                s += fmt.tabs(n) + 'case ' + indents + valStr + ': '
                s += 'return \"' + symStr + '\";\n'
        defaultSymStr = '<unknown ' + self.exportId + '>'
        if eolAfterCaseStatement:
            s += fmt.tabs(n) + 'default:\n' 
            s += fmt.tabs(n+1) + 'return ' + fmt.cstr(defaultSymStr) + '\n'
        else:
            indents = ' '*(self.valMaxStrLen - (len('default') - len('case'))) 
            s += fmt.tabs(n) + 'default: ' + indents
            s +=' return ' + fmt.cstr(defaultSymStr) + ';\n'
        n -= 1
        s += fmt.tabs(n) +'\n}\n'
        return s

    def _fmt_c_getter(self):
        s = ''
        s += 'char* get_' + self.exportId + '_asStr('+self.exportId+' v)'
        s += '\n{\n'
        return s

    def _fmt_c_lut(self):
        s = ''
        s += '/**\n' 
        s += self._fmt_c_baseComment()
        s += ' *\n'
        s += ' * Enum as sumbol name string lookup table (LUT) from enum \n'
        #s += ' * Index in LUT corresponds to least significant bit (LSB) position\n'
        #s += ' * i.e. enum with value 0x01 is mapped to index 0\n'
        #s += ' * All indexes in range 0 to FLAG_LUT_MAX is mapped to string\n'
        #s += ' * if no such enum its unknown default\n'
        s += ' */\n'
        
        if 0 in self.valMap:
            symUndefNm = self.symToStrFilt(self.valMap[0])
        else:
            symUndefNm = 'undefined_flag'
        s += '#define ' + fmt.pre + 'VALUE_LUT__' + self.exportId + '\\\n'
        s += '{\\\n'
        maxBitSet = max(self.bitFieldMap)+1
        totStrLen = 0
        for i in range(0, maxBitSet):
            bitIdxStr = str(i)
            line = fmt.tabs(1)
            indent = ' '*(len(str(maxBitSet))-len(bitIdxStr))
            line += indent + '[' + bitIdxStr + '] = '
            if i in self.bitFieldMap:
                symStr = self.symToStrFilt(self.bitFieldMap[i])
            else:
                symStr = '<' + symUndefNm + '_' + str(i) + '>'
            totStrLen += len(symStr) + 1 # + to include c null char?
            line += fmt.cstr(symStr) 
            if i < maxBitSet-1: line += ','
            else: line += ' '
            line += ' '*(self.symMaxStrLen - len(symStr))
            symValHexStr = str(hex(self.enumMap[self.bitFieldMap[i]]))
            line += '/*(' + symValHexStr + ')*/' 
            line += '\\\n'
            s += line
        s += '}\n'
        

class EnumFlagField(EnumBaseClass):
    def __init__(self, enumId, exportId = True, stripPrefix = True, acceptZero = True):
        super(EnumFlagField, self).__init__(enumId, exportId, stripPrefix)
        self.bitFieldMap = {}
        self.validFlgsMsk = 0
        errmsg = 'Enum is not a valid bit flag field. '
        for enumSym in self.enumMap:
            v = int(self.enumMap[enumSym])
            es = str(enumSym)
            if acceptZero == False and v == 0:
                errmsg += 'Zero value not accepted '+str(es)
                raise ValueError(errmsg)
            if bin(v).count('1') > 1: # bits set count > 1
                #errmsg = 'Enum is not a valid flag field.'
                errmsg += 'More then one bit set in '+str(es)
                raise ValueError(errmsg)
            if self.validFlgsMsk & v:  # Conflicting bits set
                errmsg += 'Conflicting bits set in ' + es
                raise ValueError(errmsg)
            self.validFlgsMsk |= v # Add bit to mask
            bitIdx = EnumFlagField._ffs(v)
            self.bitFieldMap[bitIdx] = es
        # success
        
    # Find first (bit) set
    def _ffs(num):
        if num == 0: return -1 # Check there is at least one bit set.
        i = 0 # Right-shift until we have the first set bit in the LSB pos
        while (num % 2) == 0:
            i += 1
            num = num >> 1
        num = num >> 1        
        return i

    # Lookup table (lut) for Flag bit position index (ffs)
    def _fmt_c_ffsLut(self):
        s = ''
        s += '/**\n' 
        s += self._fmt_c_baseComment()
        s += ' *\n'
        s += ' * Flag field lookup table (LUT) from enum \n'
        s += ' * Index in LUT corresponds to least significant bit (LSB) position\n'
        s += ' * i.e. enum with value 0x01 is mapped to index 0\n'
        s += ' * All indexes in range 0 to FLAG_LUT_MAX is mapped to string\n'
        s += ' * if no such enum its unknown default\n'
        s += ' */\n'
        
        if 0 in self.valMap:
            symUndefNm = self.symToStrFilt(self.valMap[0])
        else:
            symUndefNm = 'undefined_flag'
        s += '#define ' + fmt.pre + 'FLAG_LUT__' + self.exportId + '\\\n'
        s += '{\\\n'
        maxBitSet = max(self.bitFieldMap)+1
        totStrLen = 0
        for i in range(0, maxBitSet):
            bitIdxStr = str(i)
            line = fmt.tabs(1)
            indent = ' '*(len(str(maxBitSet))-len(bitIdxStr))
            line += indent + '[' + bitIdxStr + '] = '
            if i in self.bitFieldMap:
                symStr = self.symToStrFilt(self.bitFieldMap[i])
            else:
                symStr = '<' + symUndefNm + '_' + str(i) + '>'
            totStrLen += len(symStr) + 1 # + to include c null char?
            line += fmt.cstr(symStr) 
            if i < maxBitSet-1: line += ','
            else: line += ' '
            line += ' '*(self.symMaxStrLen - len(symStr))
            symValHexStr = str(hex(self.enumMap[self.bitFieldMap[i]]))
            line += '/*(' + symValHexStr + ')*/' 
            line += '\\\n'
            s += line
        s += '}\n'
        
        s += '\n'
        s += '/**\n' 
        s += ' * Total number of chars all strings in LUT combined.\n'
        s += ' * Typicaly used to allocate memory for a char buffer.\n'
        s += ' * Note: This value is equal sizeof(LUT), including null char but if\n'
        s += ' *       delimiter used, remeber to also allocate space for delimiter\n'
        s += ' *       i.e. sizeof(<delimiter>) *  FLAG_LUT_MAX (TODO verify!)\n'
        s += ' */\n'
        s += '#define ' + fmt.pre + 'FLAG_LUT_SIZEOF__' + self.exportId
        s += '  (' + str(totStrLen) + ')\n'

        s += '/** Max index in flag lookup table above */\n'
        s += '#define ' + fmt.pre + 'FLAG_LUT_MAX__' + self.exportId
        s += '  (' + str(maxBitSet) + ')\n'
        return s

    def _fmt_c_validator(self):
        s = '\n'
        s += '/**\n'
        s += ' * Valid flag check. \n'
        s += ' * @param  v [in] int flag field derived from enum flags\n'
        s += ' *         in ' + self.enumId + '\n'
        s += ' * @return False (0) if any bit set in param v is not a valid flag.\n'
        s += ' */\n'
        s += '#define ' + fmt.pre + 'IS_VALID_SET__' + self.exportId + '(v)\\\n'
        s +=  fmt.tab + '((v&(~' + str(hex(self.validFlgsMsk)) + ')) ? 1 : 0)'
        s += '\n'
        return s 


def doEnum(name):
    elfPath = ''
    r = gdb.execute('file ' +elfPath, False, True)
    
    if 1:
        eff = EnumFlagField(name)
        #print(eff.definedInFile)
        print(eff._fmt_c_ffsLut())
        print(eff._fmt_c_validator())
    if 0:
        ecc = EnumContCount(name)
        print(ecc._fmt_c_ternary())
        #print(ecc._fmt_c_switch())

def procExportList(exportList=None):
    s = ''
    includeGuardId = fmt.pre + 'H_' 
    s += '#ifndef ' + includeGuardId + fmt.eol
    s += '#define ' + includeGuardId + fmt.eol

    #for e in exportList:
    name = 'sysProtection_flag_t'
    eff = EnumFlagField(name)
    #print(eff.definedInFile)
    s += eff._fmt_c_ffsLut()
    s += eff._fmt_c_validator()

    ecc = EnumContCount(name)
    s += ecc._fmt_c_ternary()
    #print(ecc._fmt_c_switch())
    s += '#endif /*' + includeGuardId + '*/' + fmt.eol
    print(s)
##doEnum("lvlsChId_t")
#doEnum('sysProtection_flag_t')
procExportList()
#doEnum('sysProtectionFlag_NONE')
# info types ^lvlsChId_t$
#print(basename(typedefSrcFile("lvlsChId_t")))

#print( EnumTr.("lvlsChId_t"))
    #print( EnumTr.getEnumDictFromMember("lvlsCh_PREAL"))

#print( EnumTr.asCChrAry("lvlsChId_t", stripPrefix="lvlsCh_"))
#opt = EnumTr.Opt(enum="lvlsChId_t", trFrom=trFrom_ENUM2STR, prefix2Strip=None, outFmt=outFmt_ANSIC_SWITCH)
#print( EnumTr.fmtOut("sysState_t", "sysState_"))

'''
result = [os.path.join(dp, f) 
for dp, dn, filenames in os.walk(PATH):
    for f in filenames:
        if os.path.splitext(f)[1] == '.txt']
'''

#res = gdb.execute("p target", False, True)
#print (getSymbAddr('sched.slotIndex'))
#getEnumVal('lvlsCh_IGRID')
#PrintGList()
#w = 'sched.slotIndex'
#m = w.type.tag
#print (m)
#tp = gdb.lookup_global_symbol("g_dft_result[0].adc_buf")
#at = gdb.parse_and_eval("g_dft_result[0].adc_buf").type
#at = gdb.lookup_type(a)
#print (at)
#t = gdb.lookup_type(enumTypeDefName)
#s = gdb.lookup_symbol('sched.slotIndex',Block.global_block)
