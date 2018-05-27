def empty_env():
    return [ ]
def extend_env(var,env):
    return [var] + env
class ApplyEnvError(Exception): pass

def apply_env(env,var):
    # can translate to Tail
    print( "senv:",env,len(env),var )
    if env == [ ]:
        raise ApplyEnvError("unbound var: {}".format(var))
    elif var == env[0]:
        return 0
    else:
        return 1 + apply_env (env[1:],var)
def init_env():
    return ['i','v','x']
def apply_n_env(env,n):
    print( "nenv:",env,len(env),n )
    return env[n]
def extend_n_env(val,env):
    return [val] + env
def empty_n_env():
    return [ ]
__all__ = ["empty_env","extend_env","apply_env",
           "empty_n_env","extend_n_env","apply_n_env",
           "init_env"]
