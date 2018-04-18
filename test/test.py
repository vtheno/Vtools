#coding=utf-8
from Parsec import *
kLet = symbol(toList("let"))
kIn = symbol(toList("in"))
kEq = symbol(toList("="))
kLm = symbol(toList("\\"))
kTo = symbol(toList("->"))

Expr = type("Expr",(),{})
def app(self,e1,e2):
    self.e1 = e1
    self.e2 = e2
def app2s(self):
    return "(App {} {})".format(repr(self.e1),repr(self.e2))
App = type("App",(Expr,),{"__init__":app,"__repr__":app2s})
def lam(self,n,e):
    self.n = n
    self.e = e
def lam2s(self): return "\\{} -> {}".format(self.n,repr(self.e))
def lam2py(self): return "(lambda {} : {})".format(self.n,repr(self.e))
Lam = type("Lam",(Expr,),{"__init__":lam,"__repr__":lam2s,"topy":lam2py})
def let(self,n,e1,e2):
    self.n = n;self.e1=e1;self.e2=e2
def let2s(self): return "let {} = {} in {}".format(self.n,repr(self.e1),repr(self.e2))
Let = type("Let",(Expr,),{"__init__":let,"__repr__":let2s})
def var(self,n):
    self.n=n
def var2s(self): return "{}".format(self.n)
Var = type("Var",(Expr,),{"__init__":var,"__repr__":var2s})

Curry = lambda f:lambda a:lambda b:f(a,b)
def expr(p):
    r = chainl1(atom)(mret(App))(p)
    return r
def atom(p):
    # 1 +++ 2 +++ 3 => ((1,2),3) right 结合
    return alt1(alt1(alt1(lamp,letp),varp),paren) (p)
def lamp(p):
    #print "lamp:",repr(''.join(toPylist(p)))
    return bind( kLm ,lambda _ :
            bind( variable ,lambda n :
            bind( kTo,lambda _ :
            bind( expr,lambda e :
            mret ( Lam(n,e) ) ) ) ) ) (p)
def letp(p):
    return bind( kLet , lambda _ :
           bind( variable,lambda n :
            bind( kEq ,lambda _:
            bind( expr,lambda e1:
            bind( kIn,lambda _:
            bind( expr,lambda e2: mret( Let(n,e1,e2) ) ) ) ) ) )) (p)
def varp(p):
    r = bind(variable,lambda x:mret(Var(x)))(p)
    return r
def paren(p):
    op = symbol(toList("("))
    cl = symbol(toList(")"))
    return bracket(op)(expr)(cl)(p)
def variable(p):
    keys = toList ( [kLet,kIn,kEq,kLm,kTo] )
    result = identifier(keys)(p)
    #print "variable:",repr(''.join(toPylist(p)))
    #print "variable:",result
    return result

reade = read(expr)
test = "let c = (\\a -> a) in (\\a -> a) c"
print reade(test)
