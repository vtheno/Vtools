#coding=utf-8
from util.Match import *
from datatype import *
from env import *
from parse import *
print( dir() )
# translate_of : Exp * SEnv -> Nameless-exp
@matcher(Const_exp,False)
def translate_of(self,env):
    return self
@matcher(Const_exp,False)
def value_of(self,env):
    return Num_val(self.num)
@matcher(Var_exp,False)
def translate_of(self,env):
    return Nameless_var_exp(apply_env(env,self.var))
@matcher(Nameless_var_exp,False)
def value_of(self,env):
    return apply_n_env(env,self.n)
@matcher(Diff_exp,False)
def translate_of(self,env):
    return Diff_exp(translate_of(self.exp1,env),translate_of(self.exp2,env))
@matcher(Diff_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env) # Exp * Env -> ExpVal
    val2 = value_of(self.exp2,env) # Exp * Env -> ExpVal
    num1 = expval_num (val1) # ExpVal -> Int
    num2 = expval_num (val2) # ExpVal -> Int
    return Num_val(num1 - num2) # Int -> ExpVal
@matcher(Zerop_exp,False)
def translate_of(self,env):
    return Zerop_exp(translate_of(self.exp,env))
@matcher(Zerop_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp,env) # Exp * Env -> ExpVal 
    num1 = expval_num(val1)   # ExpVal -> Num
    if num1 == 0 : # Int * Int -> Bool
        return Bool_val(True) # Bool -> ExpVal
    else:
        return Bool_val(False) # Bool -> ExpVal
@matcher(If_exp,False)
def translate_of(self,env):
    return If_exp(translate_of(self.exp1,env),
                  translate_of(self.exp2,env),
                  translate_of(self.exp3,env))
@matcher(If_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env) # Exp * ENv -> ExpVal
    flag = expval_bool(val1) # ExpVal -> Bool
    if flag: 
        return value_of(self.exp2,env) # Exp * ENv -> ExpVal
    else:
        return value_of(self.exp3,env) # Exp * ENv -> ExpVal

@matcher(Let_exp,False)
def translate_of(self,env):
    return Nameless_let_exp(
        translate_of(self.exp1,env),
        translate_of(self.body,extend_env(self.var,env)))
@matcher(Nameless_let_exp,False)
def value_of(self,env):
    val = value_of(self.n1,env)
    #print(type(self.n1) )
    print( "letenv:",env )
    return value_of(self.n2,extend_n_env(val,env))
@matcher(Proc_exp,False)
def translate_of(self,env):
    return Nameless_proc_exp(
        translate_of(self.body,extend_env(self.var,env)))
@matcher(Nameless_proc_exp,False)
def value_of(self,env):
    return Proc_val(procedure(self.n,env))

@matcher(Call_exp,False)
def translate_of(self,env):
    return Call_exp(
        translate_of(self.exp1,env),
        translate_of(self.exp2,env))
@matcher(Call_exp,False)
def value_of(self,env):
    proc = expval_proc( value_of(self.exp1,env) )
    # expval_proc : ExpVal -> ProcVal
    # proc : ProcVal 
    arg  = value_of(self.exp2,env) # Exp * Env -> ExpVal
    return apply_procedure(proc,arg)

class Apply_Procedure_Error(Exception): pass
def apply_procedure(proc1,val):
    if isinstance(proc1,procedure):
        body = proc1.body
        env = proc1.env
        return value_of(body,extend_n_env(val,env))
    raise Apply_Procedure_Error("type({}) is not procedure".format(proc1))
def newtest():
    e = empty_n_env()
    n = empty_env()
    print( scanAndParse("66").translate_of(n).value_of(e) )
    #print( scanAndParse("abc").translate_of(n).value_of(e) )
    print( scanAndParse("-(1,2)").translate_of(n).value_of(e) )#.value_of(e) )
    print( scanAndParse("zero? 0").translate_of(n).value_of(e) )
    print( scanAndParse("""
    if zero? 0 
    then -(1,2) 
    else -(2,1)
    """).translate_of(n).value_of(e) )
    print( scanAndParse("""
    let f = 1
    in let f = 2 
       in -(f,-(0,f))
    """ ).translate_of(n).value_of(e) )
    #print( scanAndParse("""
    #let makemult = fn (maker) 
    #                  fn (x)
    #                     let a = -(0,4) in 
    #                     if zero? x 
    #                     then 0
    #                     else -( ((maker maker) -(x,1)), a)
    #in let time4 = fn (x) ( (makemult makemult) x) 
    #   in (time4 1)
    #""").translate_of(n).value_of(e) )
newtest()
def repl():
    e = empty_env()
    inp = input(">> ")
    while 1:
        if inp == ':q':
            break
        print( scanAndParse(inp).value_of(e) )
        inp = input(">> ")
#if __name__ == '__main__':
#    test()
#    repl()
