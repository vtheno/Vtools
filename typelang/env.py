empty = "empty"
extend = "extend-env"
extend_rec = "extend-env-rec"
# Env = Var -> SchemeVal
# Env = String -> PythonVal
def empty_env(): # () -> Env
    return [empty]
def extend_env(var,val,env):
    # Var * SchemeVal * Env -> Env
    # String * PythonVal * Env -> Env
    return [extend,var,val,env]
def extend_env_rec(pname,bvar,body,env):
    # Var * Var * Exp * Env ~> Env
    return [extend_rec,pname,bvar,body,env]

def car(lst): return lst[0]
def cdr(lst): return lst[1:]
def cadr(lst): return car(cdr(lst))
def caddr(lst): return car(cdr(cdr(lst)))
def cadddr(lst):return car(cdr(cdr(cdr(lst))))
class ApplyEnvError(Exception): pass
from datatype import *
from util.Match import *
@Tail
def tail_apply_env(env,search_var):
    # Env * Var -> SchemeVal
    # Env * String -> PythonVal
    if car(env) == empty:
        raise ApplyEnvError("no binding found: {}".format(search_var))
    elif car(env) == extend:
        saved_var = cadr (env) 
        saved_val = caddr (env) 
        saved_env = cadddr (env) 
        if search_var == saved_var :
            return saved_val
        else:
            return tail_apply_env(saved_env,search_var)
    # apply extend_rec
    elif car(env) == extend_rec:
        rec_env = cdr(env)
        pname = car(rec_env) # proc name : Var
        bvar  = cadr(rec_env) # proc arg : Var
        pbody = caddr(rec_env) # proc body : Expr
        saved_env = cadddr(rec_env) # Env 
        if search_var == pname :
            return Proc_val( procedure(bvar,pbody,env) )
        else:
            return tail_apply_env(saved_env,search_var)
    else:
        raise ApplyEnvError("Invalid env:{}".format(env))
def apply_env(env,search_var):
    return force( tail_apply_env(env,search_var) )
def init_env(): # () -> Env
    return extend_env('x',3,
            extend_env('y',7,
            extend_env('u',5,
            empty_env())))
__all__ = ["empty_env","extend_env","apply_env",
           "extend_env_rec",
           "init_env"]
