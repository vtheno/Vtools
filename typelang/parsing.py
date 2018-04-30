#coding=utf-8
from util.Lexical import Lexical
from util.List import *
from util.Match import matcher,force,Tail
SpecTab = toList( [ ("=",toList( [ "=",
                                   ">",
                                   "<"] ) ) ,
                   ]
                  )
Lexical = Lexical(SpecTab)
Lex = Lexical.Lex
#string = "a"*10000
#inp = Lex(string)
#print inp
from util.dt import *
d = Datatype()
c = Constructor()
d.Expression() == c.Const_exp('num') \
    | c.Diff_exp('exp1','exp2') \
    | c.Zerop_exp('exp') \
    | c.If_exp('exp1','exp2','exp3') \
    | c.Var_exp('var') \
    | c.Let_exp('var','exp1','body') \
    | c.Proc_exp('var','body') \
    | c.Call_exp('exp1','exp2') \
    | c.Letrec_exp('proc_name','bvar','proc_body','letrec_body') 
Expression = d.Expression
Const_exp = c.Const_exp # Int -> Exp
Diff_exp = c.Diff_exp   # Exp * Exp -> Exp
Zerop_exp = c.Zerop_exp # Exp -> Exp
If_exp = c.If_exp       # Exp * Exp * Exp -> Exp
Var_exp = c.Var_exp     # Var -> Exp
Let_exp = c.Let_exp     # Var * Exp * Exp -> Exp
Proc_exp = c.Proc_exp   # Var * Exp -> Exp
Call_exp = c.Call_exp   # Exp * Exp -> Exp
Letrec_exp = c.Letrec_exp # Var * Var * Exp * Exp -> Exp
@matcher(Var_exp,False)
def __eq__(self,other):
    return self.var == other
keywords = ["let","in","zero"
            "if","then","else","fn",
            "letrec","-","=","(",")",",","?"
        ]
neg ="-"
Defn ="="
lf = "("
rf = ")"
dot = ","
If = "if"
Then = "then"
Else = "else"
Let =  "let"
In  =  "in"
Zero = "zero"
pP = "?"
Fn = "fn"
LetRec = "letrec"
class ParseError(Exception): pass
def strip(tok,toks):
    if toks.null():
        raise ParseError
    else:
        with toks as (first,rest):
            if tok == first:
                return rest
            else:
                raise ParseError("stripError: {} ,{}".format(tok,toks))
def IsId(v):
    return v not in keywords and v.isalnum()
def IsNum(v):
    return v.isdigit()
@Tail
def parseVar(toks):
    if toks.null():
        raise ParseError("parseVarError: {} is null".format(toks))
    else:
        with toks as (var,rest):
            if IsId(var):
                return Var_exp(var),rest
            else:
                raise ParseError("parseVarError: {} ,{}".format(var,rest))
@Tail
def parseAtom(toks):
    with toks as (op,rest):
        if op == If:
            exp1,rest1 = force( parseExp(rest) )
            exp2,rest2 = force( parseExp( strip("then",rest1)) )
            exp3,rest3 = force( parseExp( strip("else",rest2)) )
            return If_exp(exp1,exp2,exp3),rest3
        elif op == Let:
            var1,rest1 = force( parseVar(rest) )
            exp1,rest2 = force( parseExp(strip(Defn,rest1)) )
            body,rest3 = force( parseExp(strip(In,rest2)) )
            return Let_exp(var1,exp1,body),rest3
        elif op == LetRec:
            pname,rest1 = force( parseVar(rest) )
            pvar,rest2 = force( parseVar(strip(lf,rest1) ) )
            pbody,rest3 = force( parseExp(strip(Defn,strip(rf,rest2)) ) )
            lbody,rest4 = force( parseExp(strip(In,rest3)) )
            return Letrec_exp(pname,pvar,pbody,lbody),rest4
        elif op == Zero:
            exp1,rest1 = force( parseExp( strip("?",rest) )  )
            return Zerop_exp(exp1),rest1
        elif op == Fn:
            var,rest1 = force( parseVar(strip(lf,rest)) )
            body,rest2 = force( parseExp(strip(rf,rest1) ) )
            return Proc_exp(var,body),rest2
        elif IsNum(op):
            return Const_exp(int(op)),rest
        elif IsId(op):
            return Var_exp(op),rest
        elif op == lf:
            exp1,rest1 = force( parseExp(rest) )
            #try:
            #    exp2,rest2 = force(parseExp(rest1) )
            #    return Call_exp(exp1,exp2),strip(rf,rest2)
            #except ParseError:
            #    return exp1,strip(rf,rest1)
            return exp1,strip(rf,rest1)
        else:
            raise ParseError("parseAtomError: {},{}".format(op,rest))
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
            if b == neg:
                exp2,rest = force( parseAtom(bs) )
                return parseRest( Diff_exp(exp1,exp2) ,rest)
            elif b == lf:
                exp2,rest = force( parseExp(bs) )
                return parseRest( Call_exp(exp1,exp2) ,strip(rf,rest) )
            else:
                return (exp1,toks)

def read(inp):
    output = force( parseExp(Lex(inp)) )
    with unpack(output) as (result,rest):
        if rest.null():
            return result
        else:
            raise ParseError("not all")
def test():
    print( read("66") )
    print( read("abc") )
    print( read("1 - 2") )
    print( read("zero? 0") )
    print( read("""
    if zero? 0 
    then 1 - 2
    else 2 - 1
    """) )
    print( read("""
    let a = 233
    in if zero? 0 
    then 1 - 2
    else 2 - 1
    """) )
    print( read("""
    fn (a) 233
    """) )
    print( read("""
    letrec id(x) = x
    in id (233) 
    """) )
    print( read("""
    letrec double(x) = if (zero? x)
                       then 0 
                       else (double (x - 1)) -  (0 - 2)
    in double(6)
    """) )
#test()
__all__ = ["read","test",
           "Expression","Const_exp","Diff_exp","Zerop_exp",
           "If_exp","Var_exp","Let_exp","Proc_exp","Call_exp",
           "Letrec_exp"]
