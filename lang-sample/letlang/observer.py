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
