from util.Lexical import Lexical
from util.List import *
from util.Match import matcher,force,Tail
SpecTab = toList( [ ("=",toList( [ "=",
                                   ">",
                                   "<"] ) ) ] )
# == , => , =< ,二元运算符
Lexical = Lexical(SpecTab)
Lex = Lexical.Lex
#string = "a"*10000
#inp = Lex(string)
#print inp
#from util.dt import *
#d = Datatype()
#c = Constructor()
class ParseError(Exception): pass
def strip(tok,toks):
    if toks.null():
        raise ParseError
    else:
        with toks as (first,rest):
            if tok == first:
                return rest
            else:
                raise ParseError("strip")

def IsId(v):
    return v not in ["if","then","else",
                "let","in",
            ] and v.isalnum()
def IsNum(v):
    return v.isdigit()
def IsBool(v):
    return v == 'true' or v == 'false'
class ToValueErr(Exception): pass
def ToBool(v):
    if v == 'true':
        return True
    elif v == 'false':
        return False
    raise ToValueErr("ToBool")
@Tail
def parseVar(toks):
    with toks as (var,rest):
        if IsId(var):
            return ["Id",var],rest
        else:
            raise ParseError("parseVar")
@Tail
def parseAtom(toks):
    with toks as (op,rest):
        if op == "if":
            exp1,rest1 = force( parseExp(rest) )
            exp2,rest2 = force( parseExp( strip("then",rest1)) )
            exp3,rest3 = force( parseExp( strip("else",rest2)) )
            return ["If",exp1,exp2,exp3],rest3
        elif op == "let":
            var1,rest1 = force( parseVar(rest) )
            exp1,rest2 = force( parseExp(strip("=",rest1)) )
            body,rest3 = force( parseExp(strip("in",rest2)) )
            return ["Let",var1,exp1,body],rest3
        elif IsBool(op):
            return ["Bool",ToBool(op)],rest
        elif IsNum(op):
            return ["Num",long(op)],rest
        elif IsId(op):
            return ["Id",op],rest
        elif op == '(':
            exp1,rest1 = force( parseExp(rest) )
            return exp1,strip(')',rest1)
        else:
            raise ParseError("parseAtom")
@Tail            
def parseExp(toks):
    exp1,rest1 = force( parseAtom(toks) )
    return parseRest(exp1,rest1)

@Tail
def parseRest(exp1,toks):
    if toks.null():
        return (exp1,toks)
    else:
        with toks as (b,bs):
            if b == "+":
                exp2,rest = force( parseAtom(bs) )
                return parseRest(["BinOp",exp1,b,exp2],rest)
            elif b == '-':
                exp2,rest = force( parseAtom(bs) )
                return parseRest(["BinOp",exp1,b,exp2],rest)
            else:
                return (exp1,toks)
inp = Lex("""
let b = 3 in 
if 6 + b then true else false
""")
print force( parseExp(inp) )
# if true then a else b
def read(inp):
    return force( parseExp(Lex(inp)) )
print read("""
let a = if true then 233 else 332 
in (if (let c = a + a in c + a)
    then true - 1
    else false + 1)
""")
