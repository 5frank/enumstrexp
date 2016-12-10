'''
pre processor string parser. 
'''
import shlex
import re

class BadExprException(Exception):
    pass


def parseExpr(s):
    s = str(s)
    m = re.search(r'(.*?)\((.*?)\)', s)
    if not m:
        print (s)
        raise BadExprException
    func = m.group(1)
    args = m.group(2).split(',')
    return func, args


def isStrStr(s):
    return s.startswith('"') and s.endswith('"')


def parseReReplace(args):
    predfined = ['COMMON_PREFIX', 'COMMON_SUFFIX'],
    pass

formaters = {
 'RE_REPLACE' : parseReReplace
 'RE_EXCLUDE' : None,
 'RE_INCLUDE' : None,
 'REFMT' : None,
 }

exprs = ['EXCL_M(myEnum_NUMBOF)', 'resub("c", "keso")', 'rstrip)']

for expr in exprs:
    #args = shlex.split(expr)
    print (parseExpr(expr))
    #print (args)
