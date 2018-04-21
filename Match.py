#coding=utf-8

def Tail(func):
    def call(*args,**kw): # x
        yield func (*args,**kw)
    return call
def force(g):
    while type(g).__name__ == 'generator':
        g = next(g)
    return g
def setEnv(func,typ,env):
    if func.__name__ not in env.keys():
        env[func.__name__] = {typ.__name__:func}
    else:
        if typ.__name__ not in env[func.__name__].keys():
            env[func.__name__][typ.__name__] = func
        else:
            pass#raise TypeError("SetEnv error")
    return env
def Match(Env={}):
    def matcher(typ,tail=True):
        def helper(func): 
            setEnv(func,typ,Env)
            if tail:
                setattr(typ,func.__name__,Tail(func))
            else:
                setattr(typ,func.__name__,func)
            def warp(v,*args):
                return getattr(v,func.__name__)(*args)
            return warp
        return helper
    return matcher
env = {}
matcher = Match(env)
def showMatchEnv():
    print env
__all__ = ["Tail","force","matcher","Match","showMatchEnv"]
