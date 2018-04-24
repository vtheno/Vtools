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
    |  c.letstar_exp('bindings','body_exp') \
    |  c.unpack_exp('vars','exp1','body') \
    |  c.proc_exp('var','body') \
    |  c.call_exp('rator','rand') 

# old    |  c.let_exp('var','exp1','body_exp')
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
unpack_exp = c.unpack_exp
proc_exp = c.proc_exp
call_exp = c.call_exp
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
              "cond","end","unpack",
              "proc",
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
def pUnpack(inp):
    sym = symbol(toList("unpack"))
    Vars = sepby(var)(symbol(toList(",")))
    defn = symbol(toList("="))
    In  = symbol(toList("in"))
    return bind(sym,lambda _:
        bind(Vars,lambda vars:
        bind(defn,lambda _ :
        bind(expr,lambda e1:
        bind(In,lambda _:
        bind(expr,lambda body:
        mret( unpack_exp (vars,e1,body) )))))))(inp)
def pProc(inp):
    sym = symbol(toList("proc"))
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bind(sym,lambda _:
            bind(lf,lambda _:
            bind(var,lambda v :
            bind(rf,lambda _:
            bind(expr,lambda body:
                 mret ( proc_exp(v,body) ) )))))(inp)
def pCall(inp):
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bind(lf,lambda _:
        bind(expr,lambda e1:
        bind(expr,lambda e2:
        bind(rf,lambda _:
             mret( call_exp(e1,e2) ) ))))(inp)
def Expr(inp):
    # 带 key 关键词的 解析优先级在上方 
    return \
           alt(pCall)(
           alt(pProc)(
           alt(letexp)(
           alt(letstar)(
           alt(pUnpack)(
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
           alt(var)(const)  )))))))))))))))))))(inp)
def paren(inp):
    lf = symbol(toList("("))
    rf = symbol(toList(")"))
    return bracket(lf)(Expr)(rf)(inp)
def expr(inp):
    #return alt(paren)(Expr)(inp)
    return alt1(Expr,paren)(inp)
dt.expval('a') == c.num_val('num') \
    | c.bool_val('bool') \
    | c.cons_val('hd','tl') \
    | c.nil_val() \
    | c.proc_val('proc') 
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
proc_val = c.proc_val
dt.proc() == c.procedure('var','body','saved_env')
Proc = dt.proc
procedure = c.procedure
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
def expval2nilp(v):
    if isinstance(v,nil_val):
        return True
    if isinstance(v,cons_val):
        return False
    raiseError("expval->nil?: {}".format(v))
def expval2car(v):
    if isinstance(v,cons_val):
        return v.hd
    raiseError("expval->car: {}".format(v))
def expval2cdr(v):
    if isinstance(v,cons_val):
        return v.tl
    raiseError("expval->cdr: {}".format(v))
def expval2nil(v):
    if isinstance(v,nil_val):
        return nil
    raiseError("expval->nil: {}".format(v))
def exp_cons2Cons(v):
    if isinstance(v,nil_val):
        return nil
    if isinstance(v,cons_val):
        return Cons(v.hd,exp_cons2Cons(v.tl))
    raiseError("expval->cons: {}".format(v))
def expval2proc(v):
    if isinstance(v,proc_val):
        return v.proc
    raiseError("expval->proc: {}".format(v))
#def procedure(var,body,env):
#    return lambda val : value_of(body,extend_env(var,val,env))
#def apply_procedure(procl,val):
#    return procl(val)
def apply_procedure(procl,val):
    if isinstance(procl,Proc):
        return value_of(procl.body,extend_env(procl.var,val,procl.saved_env))
    raiseError("apply-procedure: {}".format(v))

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
        raise Exception("no binding found {}".format(search_var))
    elif car(env) == extend:
        saved_var = cadr(env)
        saved_val = caddr(env)
        saved_env = cadddr(env)
        if search_var == saved_var:
            return saved_val
        else:
            return apply_env(saved_env,search_var)
    else:
        raise Exception("invaild env {}".format(env))
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
@matcher(minus_exp,False)
def value_of(self,env):
    val1 = self.exp1.value_of(env)
    num1 = expval2num(val1)
    return num_val(-num1)
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
    return nil_val()#expval2nil(nil_val())
@matcher(cons_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env)
    val2 = value_of(self.exp2,env)
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
    #print "nullp:",val1
    v1 = expval2nilp(val1)
    if v1:
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
    """
    vals = foldr(lambda hd,end: Cons(value_of(hd[1],env),end),
                 nil,
                 self.bindings)
    Vars = UnZip(self.bindings)[0]
    #print vals,Vars
    env = foldr(lambda a,end:extend_env(a[0],a[1],end),
                env,
                Zip(Vars,vals))
    return value_of(self.body_exp,env)
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
    """ 
@matcher(letstar_exp,False)
def value_of(self,env):
    hd = self.bindings.hd
    var,exp = hd
    val = value_of(exp,env)
    env = extend_env(var,val,empty_env())
    newEnv = foldr(lambda hd,end: extend_env(hd[0],value_of(hd[1],env),end),
                   env,
                   self.bindings.tl)
    return value_of(self.body_exp,newEnv)
@matcher(unpack_exp,False)
def value_of(self,env):
    # self.vars,self.exp1 ,self.body
    val = value_of(self.exp1,env)
    v1 = exp_cons2Cons(val)
    #print type(v1),v1
    lv,le = length(self.vars) ,length(v1)
    if lv != le :
        raise Exception("unpack list no equal, length vars: {} ,length expression: {}".format(lv,le))
    else:
        bindings = Zip(self.vars,v1)
        env = foldr(lambda a,end:extend_env(a[0],a[1],end),
                    env,
                    bindings)
        return value_of(self.body,env)
@matcher(proc_exp,False)
def value_of(self,env):
    return proc_val(procedure(self.var,self.body,env))
@matcher(call_exp,False)
def value_of(self,env):
    procl = expval2proc(value_of(self.rator,env))
    arg = value_of(self.rand,env)
    return apply_procedure(procl,arg)
init = init_env()
empty = empty_env()
