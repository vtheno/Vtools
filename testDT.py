#coding=utf-8
from Parsec import *
print( dir() )
kData = toList("datatype")
kEq   = toList("=")
kOr   = toList("|")
kOf   = toList("of")
kDot  = toList("*")
keys = toList ( [kData,kEq,kOr,kOf,kDot] )
Constructor = type("Constructor",(),{})
def CTinit(self,name,*typename):
    self.name = name
    self.typename = list(typename)
def CT2s(self):
    if self.typename != ():
        return "{} of {}".format(self.name,self.typename)
    return "{}".format(self.name)
def CT2py(self):
    name = ''.join(toPylist(self.name))
    temp = """
def {name}Init(self): pass
"""
    template = "{name} = type({name1},({super},),{env})"
    temp2 = """
def {name}Init(self,{args}):
{sets}
"""
    env = r"{l} '__init__':{name}Init,{r}".format(l="{",r="}",name=name)
    if self.typename == []:
        return lambda super:(temp + template).format(name=name,name1=repr(name),env=env,super=super)
    else:
        List = self.typename[0]
        lst = toPylist(List)
        lst = map(lambda x:''.join(toPylist(x)),lst)
        print( "lst:",lst,map(type,lst) )
        args = ",".join(lst)
        tmp = map(lambda v:"    self.{v} = {v}".format(v=v),lst)
        sets = "\n".join(tmp)
        print( sets )
        temp2 = temp2.format(name=name,args=args,sets=sets)
        return lambda super : (temp2 + template).format(name=name,name1=repr(name),env=env,super=super)
CT = type("Constructor",(Constructor,),
          {"__init__":CTinit,
           "__repr__":CT2s,
           "toPy":CT2py,
       })
Expr = type("Expr",(),{})
def DataInit(self,name,*constructor):
    self.name = name
    self.constructor = constructor # construcotr
def Data2s(self):
    tmp = ' | '.join(map(repr,self.constructor))
    return "datatype {} = {}".format(self.name,tmp)
def Data2py(self):
    name = toPylist(self.name)
    name = ''.join(name)
    env = "{}"
    temp = "{name} = type({name1},(),{env})".format(name=name,name1=repr(name),env=env)
    cs = [toPylist(i) for i in self.constructor][0]
    r = ""
    for i in cs:
        r+=i.toPy()(name)
    return temp + r
Data = type("Data",(Expr,),
            {"__init__":DataInit,
             "__repr__":Data2s,
             "toPy":Data2py,
         })
print( Data("Nat",CT("Zero"),CT("Succ","Nat")) )

def variable(inp):
    return identifier(keys)(inp)
def pvar(inp):
    return bind(variable,lambda v : mret( Var(v) ) )(inp)
sp = sepby(variable)(symbol(kDot))
#print sp("a * b * c")

def pCTof(inp):
    return bind(variable,lambda name:
            bind(symbol(kOf),lambda _ :
            bind(sp,lambda args : 
                mret ( CT(name,args) ) ) ) ) (inp)
def pCT(inp):
    return bind(variable,lambda name : mret( CT (name) ) )(inp)
def pC(inp):
    return alt1(pCTof,pCT)(inp)
pCt = read(pC)
print( pCt("nat of a * b * c") )
def pDataType(inp):
    return bind(parse(symbol(kData)),lambda _ :
            bind(variable,lambda name : 
            bind(symbol(kEq),lambda _ :
            bind(sepby1(pC)(symbol(kOr)),lambda v : 
            mret ( Data(name,v) )))))(inp)
data = read(pDataType)
t = data("datatype Nat = Zero | Succ of Nat * b")
print( t )
code = t.toPy()
print( code )
def mylang(func):
    filename = func.__name__
    code = func.__doc__
    temp = data(code)
    code = temp.toPy()
    c=compile(code,filename,"exec")
    env = {}
    eval(c,env)
    tmp = type(filename,(),env)
    def pseudo_module(kls):
        "from https://mattvonrocketstein.github.io/heredoc/python-class-as-module.html"
        import new, sys
        mod = new.module(kls.__name__, kls.__doc__)
        mod.__dict__.update(kls.__dict__)
        sys.modules[kls.__name__] = mod
        return mod
    return pseudo_module(tmp)

@mylang
def Nat():
    """
    datatype Nat = Zero
                 | Succ of Nat
    """
print( Nat )
print( Nat.Succ )
print( Nat.Zero )
print( dir(Nat) )
from Nat import *
print( Nat,Succ,Zero )
@matcher(Zero,False)
def add1(self):
    return Succ(self)
@matcher(Succ,False)
def add1(self):
    return Succ(self)
one = Succ(Zero())
two = Succ(one)
print( one )
@matcher(Zero)
def toInt(self,acc):
    return acc
@matcher(Succ)
def toInt(self,acc):
    return self.Nat.toInt(acc + 1)
def Int(nat):
    return force(toInt(nat,0))
print( Int(one) )
print( Int(two) )
