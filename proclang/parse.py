from util.dt import *

dt = Datatype()
c = Constructor()
dt.Program('exp1') == c.a_Program('exp1')
Program = dt.Program
a_Program = c.a_Program
dt.Expression() == c.Const_exp('num') \
    | c.Diff_exp('exp1','exp2') \
    | c.Zerop_exp('exp') \
    | c.If_exp('exp1','exp2','exp3') \
    | c.Var_exp('var') \
    | c.Let_exp('var','exp1','body') \
    | c.Proc_exp('var','body') \
    | c.Call_exp('exp1','exp2') 
Expression = dt.Expression
Const_exp = c.Const_exp # Int -> Exp
Diff_exp = c.Diff_exp   # Exp * Exp -> Exp
Zerop_exp = c.Zerop_exp # Exp -> Exp
If_exp = c.If_exp       # Exp * Exp * Exp -> Exp
Var_exp = c.Var_exp     # Var -> Exp
Let_exp = c.Let_exp     # Var * Exp * Exp -> Exp
Proc_exp = c.Proc_exp   # Var * Exp -> Exp
Call_exp = c.Call_exp   # Exp * Exp -> Exp
from util.Parsec import *
from util.List import toList,toPylist
keywords = ["let","in","zero?",
            "if","then","else","fn",
        ]
neg = symbol(toList("-"))
defn = symbol(toList("="))
lf = symbol(toList("("))
rf = symbol(toList(")"))
dot = symbol(toList(","))
If = symbol(toList("if"))
Then = symbol(toList("then"))
Else = symbol(toList("else"))
Let =  symbol(toList("let"))
In  =  symbol(toList("in"))
Zerop = symbol(toList("zero?"))
Fn = symbol(toList("fn"))
def number(inp):
    return token(nat)(inp)
def pConst(inp):
    return bind(number,lambda num:
                mret( Const_exp(num) ) )(inp)
def pDiff(inp):
    return bind(neg,lambda _:
            bind(lf,lambda _:
            bind(expr,lambda e1:
            bind(dot,lambda _:
            bind(expr,lambda e2:
            bind(rf,lambda _:
                 mret( Diff_exp(e1,e2) ) ))))))(inp)
def pZerop(inp):
    return bind(Zerop,lambda _:
            bind(expr,lambda e1:
                 mret( Zerop_exp(e1) )))(inp)
def pIf(inp):
    return bind(If,lambda _:
            bind(expr,lambda e1:
            bind(Then,lambda _:
            bind(expr,lambda e2:
            bind(Else,lambda _:
            bind(expr,lambda e3:
                 mret( If_exp(e1,e2,e3) ) ))))))(inp)
def pLet(inp):
    return bind(Let,lambda _:
            bind(pVar,lambda v:
            bind(defn,lambda _:
            bind(expr,lambda e1:
            bind(In,lambda _:
            bind(expr,lambda body:
                 mret ( Let_exp(v,e1,body) ) ))))))(inp)
def pProc(inp):
    return bind(Fn,lambda _:
            bind(lf,lambda _:
            bind(pVar,lambda v:
            bind(rf,lambda _:
            bind(expr,lambda body:
                 mret( Proc_exp(v,body) ) )))))(inp)
def pCall(inp):
    return bind(lf,lambda _:
            bind(expr,lambda e1:
            bind(expr,lambda e2:
            bind(rf,lambda _:
                 mret( Call_exp(e1,e2) ) ))))(inp)

def variable(inp):
    keylist = toList(list(map(toList,keywords)))
    return identifier(keylist)(inp)
def pVar(inp):
    return bind(variable,lambda e:
                mret ( Var_exp(''.join(toPylist(e)) ) ) )(inp)
def pExpr(inp):
    return \
        alt(pCall)(
        alt(pProc)(
        alt(pIf)(
        alt(pLet)(
        alt(pZerop)(
        alt(pDiff)(
        alt(pConst)(pVar) ))))))(inp)
def paren(inp):
    bk = bracket(lf)(pExpr)(rf)
    return bk(inp)
def expr(inp):
    return alt1(pExpr,paren)(inp)
from util.Match import matcher
@matcher(Var_exp,False)
def __eq__(self,other):
    return self.var == other
def test():
    print( read(expr)("66") )
    print( read(expr)("abc") )
    print( read(expr)("-(1,2)") )
    print( read(expr)("zero? 0") )
    print( read(expr)("""
    if zero? 0 
    then -(1,2) 
    else -(2,1)
    """) )
    print( read(expr)("""
    let a = 233
    in if zero? 0 
    then -(1,2)
    else -(2,1) 
    """) )
    print( read(expr)("""
    fn (a) 233
    """) )
def scanAndParse(inp):
    return read(expr)(inp)
__all__ = ["Program","a_Program","scanAndParse","test",
           "Expression","Const_exp","Diff_exp","Zerop_exp",
           "If_exp","Var_exp","Let_exp","Proc_exp","Call_exp",
]
