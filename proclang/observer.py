#coding=utf-8
from util.Match import *
from datatype import *
from env import *
from parse import *
print( dir() )
# eopl page 71
# value_of : Exp * Env -> ExpVal
@matcher(Const_exp,False)
def value_of(self,env):
    return Num_val(self.num)
@matcher(Var_exp,False)
def value_of(self,env):
    return apply_env(env,self.var)
@matcher(Diff_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env) # Exp * Env -> ExpVal
    val2 = value_of(self.exp2,env) # Exp * Env -> ExpVal
    num1 = expval_num (val1) # ExpVal -> Int
    num2 = expval_num (val2) # ExpVal -> Int
    return Num_val(num1 - num2) # Int -> ExpVal
@matcher(Zerop_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp,env) # Exp * Env -> ExpVal 
    num1 = expval_num(val1)   # ExpVal -> Num
    if num1 == 0 : # Int * Int -> Bool
        return Bool_val(True) # Bool -> ExpVal
    else:
        return Bool_val(False) # Bool -> ExpVal
@matcher(If_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env) # Exp * ENv -> ExpVal
    flag = expval_bool(val1) # ExpVal -> Bool
    if flag: 
        return value_of(self.exp2,env) # Exp * ENv -> ExpVal
    else:
        return value_of(self.exp3,env) # Exp * ENv -> ExpVal
@matcher(Let_exp,False)
def value_of(self,env):
    val1 = value_of(self.exp1,env) # Exp * ENv -> ExpVal
    # (extend_env self.var val1 env)
    # : Var * ExpVal * Env -> Env
    # value_of self.body newEnv # Exp * ENv -> ExpVal
    newEnv = extend_env(self.var,val1,env) # Env
    return value_of(self.body,newEnv)

class Apply_Procedure_Error(Exception): pass
def apply_procedure(proc1,val):
    # ProcVal * ExpVal -> ExpVal
    if isinstance(proc1,procedure):
        var,body,saved_env = proc1.var,proc1.body,proc1.env
        return value_of(body,extend_env(var,val,saved_env))
    raise Apply_Procedure_Error("type({}) is not procedure".format(proc1))
@matcher(Proc_exp,False)
def value_of(self,env):
    return Proc_val(procedure(self.var,self.body,env))
@matcher(Call_exp,False)
def value_of(self,env):
    proc = expval_proc( value_of(self.exp1,env) )
    arg  = value_of(self.exp2,env)
    return apply_procedure(proc,arg)
def test():
    e = empty_env()
    print( scanAndParse("66").value_of(e) )
    #print( scanAndParse("abc").value_of(e) )
    print( scanAndParse("-(1,2)").value_of(e) )
    print( scanAndParse("zero? 0").value_of(e) )
    print( scanAndParse("""
    if zero? 0 
    then -(1,2) 
    else -(2,1)
    """).value_of(e) )
    print( scanAndParse("""
    let a = 1
    in if zero? a 
    then -(1,2)
    else -(2,1) 
    """).value_of(e) )
    print( scanAndParse("""
    let a = 0
    in if zero? a
    then let b = -(a,1)
         in  -(b,b) 
    else a
    """).value_of(e) )
    print( scanAndParse("""
    let f = fn(a) -(a,1)
    in (f 1)
    """ ).value_of(e) )
    print( scanAndParse("""
    let makemult = fn (maker) 
                      fn (x)
                         let a = -(0,4) in 
                         if zero? x 
                         then 0
                         else -( ((maker maker) -(x,1)), a)
    in let time4 = fn (x) ( (makemult makemult) x) 
       in (time4 1)
    """).value_of(e) )
def repl():
    e = empty_env()
    inp = input(">> ")
    while 1:
        if inp == ':q':
            break
        print( scanAndParse(inp).value_of(e) )
        inp = input(">> ")
if __name__ == '__main__':
    test()
    repl()
