#coding=utf-8
#from List import toList,toPylist
from List import *
from Match import *
from Parsec import *
from dt import *
dt = Datatype()
c = Constructor()
dt.program('a') == c.a_program('exp')
program = dt.program
a_program = c.a_program
is_program = lambda x:isinstance(x,program)
dt.expression('a') ==  \
    c.const_exp('num') \
    |  c.var_exp('var') \
    |  c.minus_exp('exp1') \
    |  c.zerop_exp('exp1') \
    |  c.greatep_exp('exp1','exp2') \
    |  c.lessp_exp('exp1','exp2')  \
    |  c.equalp_exp('exp1','exp2') \
    |  c.diff_exp('exp1','exp2') \
    |  c.cons_exp('exp1','exp2') \
    |  c.nil_exp() \
    |  c.nullp_exp('exp1')  \
    |  c.car_exp('exp1') \
    |  c.cdr_exp('exp1')  \
    |  c.list_exp('args') \
    |  c.cond_exp('tups') \
    |  c.if_exp('exp1','exp2','exp3') \
    |  c.let_exp('bindings','body_exp')  \
    |  c.letstar_exp('bindings','body_exp')
#old    |  c.let_exp('var','exp1','body_exp')
# exp1 <=> of expression
# var  <=> of String
# num  <=> of int expval 
# args <=> of expression list
# tups <=> of expression * expression list
# cond { expression ==> expression }* end
# bindings <=> String * expression list
# let { identifier = expression }* in expression 
expression = dt.expression
is_expression = lambda x : isinstance(x,expression)
const_exp = c.const_exp
zerop_exp = c.zerop_exp
if_exp    = c.if_exp
diff_exp  = c.diff_exp
minus_exp = c.minus_exp
equalp_exp = c.equalp_exp
greatep_exp = c.greatep_exp
lessp_exp = c.lessp_exp
cons_exp = c.cons_exp
nil_exp  = c.nil_exp
nullp_exp = c.nullp_exp
car_exp  = c.car_exp
cdr_exp  = c.cdr_exp
list_exp = c.list_exp
cond_exp = c.cond_exp
var_exp   = c.var_exp
let_exp   = c.let_exp
letstar_exp   = c.letstar_exp
def number(inp):
    return token(nat)(inp)
def const(inp):
    return bind(number,lambda num: mret( const_exp(num) ))(inp)
def diff(inp):
    neg = symbol(toList("-"))
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bind(neg,lambda _:
            bind(lf,lambda _ :
            bind(expr,lambda e1 : 
            bind(expr,lambda e2 :
            bind(rf,lambda _ :
                 mret (diff_exp(e1,e2))  )))))(inp)
def minus(inp):
    sym = symbol(toList("minus"))
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bind(sym,lambda _ :
        bind(lf,lambda _ :
        bind(expr,lambda e:
        bind(rf,lambda _ :
             mret ( minus_exp(e) ) ))))(inp)
def zerop(inp):
    zp = symbol(toList("zero?"))
    return bind(zp,lambda _:
            bind(expr,lambda e: mret(zerop_exp(e))))(inp)
def greatep(inp):
    gp = symbol(toList("greate?"))
    return bind(gp,lambda _:
            bind(expr,lambda e1:
            bind(expr,lambda e2:
            mret ( greatep_exp(e1,e2) ) )))(inp)
def lessp(inp):
    lp = symbol(toList("less?"))
    return bind(lp,lambda _:
            bind(expr,lambda e1:
            bind(expr,lambda e2:
            mret ( lessp_exp(e1,e2) ) )))(inp)
def equalp(inp):
    ep = symbol(toList("equal?"))
    return bind(ep,lambda _:
            bind(expr,lambda e1:
            bind(expr,lambda e2:
            mret( equalp_exp(e1,e2) ) )))(inp)
def pnil(inp):
    sym = symbol(toList("nil"))
    return bind(sym,lambda _ : mret( nil_exp() ) )(inp)
def pcons(inp):
    sym = symbol(toList("cons"))
    return bind(sym,lambda _:
            bind(expr,lambda e1:
            bind(expr,lambda e2:
            mret( cons_exp(e1,e2) ))))(inp)
def pcar(inp):
    sym = symbol(toList("car"))
    return bind(sym,lambda _ :
            bind(expr,lambda e:
                 mret( car_exp(e) )))(inp)
def pcdr(inp):
    sym = symbol(toList("cdr"))
    return bind(sym,lambda _ :
            bind(expr,lambda e:
                 mret( cdr_exp(e) )))(inp)
def plist(inp):
    sym = symbol(toList("list"))
    sp = sepby(expr)(symbol(toList(",")))
    return bind(sym,lambda _:
            bind(sp,lambda args:
                 mret( list_exp(args) )))(inp)
def pcond(inp):
    sym = symbol(toList("cond"))
    end = symbol(toList("end"))
    #els = symbol(toList("else"))
    T  = symbol(toList("==>"))
    to = bind(expr,lambda e1 :
          bind(T,lambda _ :
          bind(expr,lambda e2:
               mret( (e1,e2) ) )))
    return bind(sym,lambda _ :
            bind( many1(to),lambda tup:
            bind(end,lambda _ :
                 mret( cond_exp(tup) ))))(inp)
def nullp(inp):
    sym = symbol(toList("null?"))
    return bind(sym,lambda _:
            bind(expr,lambda e:
                 mret( nullp_exp(e) )))(inp)
def ifexp(inp):
    i = symbol(toList("if"))
    then = symbol(toList("then"))
    els  = symbol(toList("else"))
    return  bind(i    , lambda _ :
            bind(expr , lambda e1 : 
            bind(then , lambda _ :
            bind(expr , lambda e2 :
            bind(els  , lambda _ :
            bind(expr , lambda e3 :
                  mret( if_exp(e1,e2,e3) ) ))))))(inp)
def variable(inp):
    keylst = ["minus","zero?",
              "equal?","greate?","less?",
              "cons","nil",
              "car","cdr","null?","list",
              "cond","end",
              "let","let*","in","if","then","else"]
    keylst = toList(list(map(toList,keylst)))
    return identifier(keylst)(inp)
def var(inp):
    return bind(variable,lambda e:
                mret ( var_exp(''.join(toPylist(e))) ))(inp)
def letexp(inp):
    let = symbol(toList("let"))
    defn = symbol(toList("="))
    In  = symbol(toList("in"))
    bindings = bind(var,lambda v:
                bind(defn,lambda _:
                bind(expr,lambda e:
                     mret( (v,e) ))))
    return bind(let,lambda _:
            bind(many1(bindings),lambda tups:
            bind(In,lambda _:
            bind(expr,lambda body:
            mret( let_exp(tups,body) )))))(inp)
def letstar(inp):
    let = symbol(toList("let*"))
    defn = symbol(toList("="))
    In  = symbol(toList("in"))
    bindings = bind(var,lambda v:
                bind(defn,lambda _:
                bind(expr,lambda e:
                     mret( (v,e) ))))
    return bind(let,lambda _:
            bind(many1(bindings),lambda tups:
            bind(In,lambda _:
            bind(expr,lambda body:
            mret( letstar_exp(tups,body) )))))(inp)
def Expr(inp):
    # 带 key 关键词的 解析优先级在上方 
    return alt(letexp)(
           alt(plist)(
           alt(ifexp)(
           alt(pcond)(
           alt(zerop)(
           alt(greatep)(
           alt(lessp)(
           alt(equalp)(
           alt(nullp)(
           alt(diff)(
           alt(minus)(
           alt(pcar)(
           alt(pcdr)(
           alt(pcons)(
           alt(pnil)(
           alt(var)(const)  )))))))))))))))(inp)
def paren(inp):
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bracket(lf)(Expr)(rf)(inp)
def expr(inp):
    #return alt(paren)(Expr)(inp)
    return alt1(Expr,paren)(inp)
#print( read(const)("123").num )
#print( "diff:",read(diff)(" - ( 1 2 ) " ) )
#print( "zero?:",read(zerop)("zero? 0") )
#print( "if then else:",read(ifexp)("if 66 then 2 else 3") )
#print( "var",read(var)("then1") )
#print( "letexp:",read(letexp)("let aaa = 1 in 233") )
#print( "expr:",read(expr)("let a = 1 in 233") )
#print( "expr2:",read(expr)("let a = 1 in a") )
dt.expval('a') == c.num_val('num') \
    | c.bool_val('bool') \
    | c.cons_val('hd','tl') \
    | c.nil_val()
 #number
 #bool
 # expval expval
expval = dt.expval
is_expval = lambda x:isinstance(x,expval)
num_val = c.num_val
bool_val = c.bool_val
cons_val = c.cons_val
nil_val = c.nil_val
nilVal = nil_val()
def raiseError(msg):
    class expvalError(Exception): pass
    raise expvalError(msg)
def expval2num(v):
    if isinstance(v,num_val):
        return v.num
    raiseError("expval->num: {}".format(v))
def expval2bool(v):
    if isinstance(v,bool_val):
        return v.bool
    raiseError("expval->bool: {}".format(v))
def expval2cons(v):
    if isinstance(v,cons_val):
        return [v.hd] + v.tl
    raiseError("expval->cons: {}".format(v))
def expval2car(v):
    if isinstance(v,cons_val):
        return v.hd
    raiseError("expval->car: {}".format(v))
def expval2cdr(v):
    if isinstance(v,cons_val):
        return v.hd
    raiseError("expval->cdr: {}".format(v))
def expval2nil(v):
    if isinstance(v,nil_val):
        return [ ]
    raiseError("expval->nil: {}".format(v))

def car(lst): return lst[0]
def cdr(lst): return lst[1:]
def cadr(lst): return car(cdr(lst))
def caddr(lst): return car(cdr(cdr(lst)))
def cadddr(lst): return car(cdr(cdr(cdr(lst))))
def empty_env():
    return ['empty']
def extend_env(var,val,env):
    return ["extend-env",var,val,env]
def apply_env(env,search_var):
    empty = 'empty'
    extend = 'extend-env'
    if car(env) == empty:
        raise "no binding found {}".format(search_var)
    elif car(env) == extend:
        saved_var = cadr(env)
        saved_val = caddr(env)
        saved_env = cadddr(env)
        if search_var == saved_var:
            return saved_val
        else:
            return apply_env(saved_env,search_var)
    else:
        raise "invaild env {}".format(env)
def init_env():
    return extend_env("i",num_val(1),
                      extend_env("v",num_val(5),
                                 extend_env("x",num_val(10),empty_env())))
@matcher(var_exp,False)
def __eq__(self,t):
    return self.var == t
@matcher(const_exp,False)
def value_of(self,env):
    return num_val(self.num)
@matcher(var_exp,False)
def value_of(self,env):
    return apply_env(env,self.var)
@matcher(diff_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    val2 = self.exp2.value_of(env)
    num1 = expval2num(val1)
    num2 = expval2num(val2)
    return num_val(num1 - num2)
@matcher(nil_exp,False)
def value_of(self,env):
    return expval2nil(nil_val())
@matcher(cons_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    val2 = self.exp2.value_of(env)
    return cons_val(val1,val2)
@matcher(list_exp,False)
def value_of(self,env):
    return value_of(foldr(cons_exp,nil_exp(),self.args),env)
@matcher(cond_exp,False)
def value_of(self,env):
    #conds,acts = UnZip(self.tups)
    """
    for cond,act in toPylist(self.tups):
        if expval2bool(value_of(cond,env)):
            return value_of(act,env)
    else:
        raiseError("no cond be true")
    """
    @Tail
    def Tail_value_Cond(lst):
        if null(lst):
            raiseError("no cond be true")
        else:
            cond,act = lst.hd
            val = value_of(cond,env)
            if expval2bool(val):
                return value_of(act,env)
            return Tail_value_Cond(lst.tl)
    t = lambda lst:force(Tail_value_Cond(reverse(lst)))
    return t(self.tups)
@matcher(nullp_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    v1 = expval2cons(val1)
    if v1 == [ ]:
        return bool_val(True)
    else: 
        return bool_val(False)
@matcher(car_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    return expval2car(val1)
@matcher(cdr_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    return expval2cdr(val1)
@matcher(zerop_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    num1 = expval2num(val1)
    if num1 == 0:
        return bool_val(True)
    else:
        return bool_val(False)
@matcher(equalp_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    val2 = self.exp2.value_of(env)
    num1 = expval2num(val1)
    num2 = expval2num(val2)
    if num1 == num2 :
        return bool_val(True)
    else:
        return bool_val(False)
@matcher(greatep_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    val2 = self.exp2.value_of(env)
    num1 = expval2num(val1)
    num2 = expval2num(val2)
    if num1 > num2 :
        return bool_val(True)
    else:
        return bool_val(False)
@matcher(lessp_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    val2 = self.exp2.value_of(env)
    num1 = expval2num(val1)
    num2 = expval2num(val2)
    if num1 < num2 :
        return bool_val(True)
    else:
        return bool_val(False)
@matcher(if_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    if expval2bool(val1) :
        return self.exp2.value_of(env)
    return self.exp3.value_of(env)
@matcher(let_exp,False)
def value_of(self,env):
    """old
    val1 = self.exp1.value_of(env)
    return self.body_exp.value_of( extend_env(self.var,val1,env) )
    @Tail
    def Tail_value_Cond(lst):
        if null(lst):
            raiseError("no cond be true")
        else:
            cond,act = lst.hd
            val = value_of(cond,env)
            if expval2bool(val):
                return value_of(act,env)
            return Tail_value_Cond(lst.tl)
    t = lambda lst:force(Tail_value_Cond(reverse(lst)))
    """
    @Tail
    def tempf(lst,acc):
        if null(lst):
            return value_of(self.body_exp, acc )
        else:
            var1,exp1 = lst.hd
            val1 = value_of(exp1,acc)
            return tempf(lst.tl,extend_env(var1,val1,acc))
    f = lambda lst : force(tempf(reverse(lst),env))
    return f(self.bindings)
@matcher(minus_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    num1 = expval2num(val1)
    return num_val(-num1)
init = init_env()
#print( "expr4:",read(expr)("let a = 1 in ( if ( zero? a ) then a else 233 )").value_of(init) )
#print( "expr5:",read(expr)(
#"""
#let a = 1 in 
#( if ( zero? a )
#      then a 
#      else -( 233 a) )
#""").value_of(init) )
#print( "expr6:",read(expr)("- (- ( x 3 ) -(v i)) ").value_of(init) )
#print( "expr7:",\
#    read(expr)("""
#let x = 7
#in let y = 2
#    in let y = let x = -(x 1)
#               in -(x y)
#    in - (-(x 8) y) 
#""").value_of(init) )
## x = 7 , y = 2 
## x2 = x - 1 = 6, y2 = x2 - 1 = 5
#print( "ift:",read(expr)("""
#if zero? 0
#then if zero? 0
#     then 3
#     else 2
#else 1 
#""").value_of(init) )
#print( read(expr)("minus(1)").value_of(init) )
#print( read(expr)("minus(-(minus(5) 9))").value_of(empty_env()) )
#print( read(expr)("equal? 1 1").value_of(init) )
#print( read(expr)("greate? 1 1").value_of(init) )
#
#print( read(expr)("""
#let a = 1 in 
#if zero? a
#then a
#else if greate? minus(a) a
#     then minus(a)
#     else let b = minus(a) in 
#          if less? a b then a else b
#""").value_of(init) )
#print( "---------------" )
#print( read(expr)("cons 1 nil") )
#print( read(expr)(
#    """
#let x = 4 in
#cons x cons -(x 1) nil
#""").value_of(init) )
#print( read(expr)(
#    """
#let x = 4 in
#cons x 
#     cons cons -(x 1) 
#               nil 
#          nil
#""").value_of(init) )
#print( read(expr)("cdr cons 1 nil").value_of(init) )
#print( read(expr)("null? (cons 1 nil)").value_of(init) )
#print( read(expr)("list 1,2,3").value_of(init)  )
#print( read(expr)("""
#let x = 4 
#in list if greate? x 2 then minus(x) else x,-(x 1),-(x 3)
#""").value_of(init)  )
#print( read(expr)("""
#let x = 4 
#in list if greate? x 2 then minus(x) else x,let c = -(x 1) in c,-(x 3)
#""").value_of(init)  )
#print( read(expr)("""
#cond (less? 2 2) ==> 2 
#     (less? 2 2) ==> 4
#     zero? 0     ==> let x = 233 in x
#end
#""").value_of(init) )
print ( read(expr)("""
let x = 30
in let x = -(x 1)
       y = -(x 2)
   in -(x y) 
""" ).value_of(init) )
print( read(letstar)("""
let*
 a = 233
 b = 234
in -(a b)""") )

