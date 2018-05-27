empty = "empty"
extend = "extend-env"
# Env = Var -> SchemeVal
# Env = String -> PythonVal
def empty_env(): # () -> Env
    return [empty]
def extend_env(var,val,env):
    # Var * SchemeVal * Env -> Env
    # String * PythonVal * Env -> Env
    return [extend,var,val,env]
def car(lst): return lst[0]
def cdr(lst): return lst[1:]
def cadr(lst): return car(cdr(lst))
def caddr(lst): return car(cdr(cdr(lst)))
def cadddr(lst):return car(cdr(cdr(cdr(lst))))
class ApplyEnvError(Exception): pass
def apply_env(env,search_var):
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
            return apply_env(saved_env,search_var)
    else:
        raise ApplyEnvError("Invalid env:{}".format(env))
def init_env(): # () -> Env
    return extend_env('x',3,
            extend_env('y',7,
            extend_env('u',5,
            empty_env())))
__all__ = ["empty_env","extend_env","apply_env",
           "init_env"]
