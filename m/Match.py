#coding=utf-8

class TailRet(object) :
    def __init__(self,call,*args, **kw) :
        self.call = call
        self.args = args
        self.kw = kw
    def handle(self,obj):
        print "self.call:",self.call,obj,self.args,self.kw
        if type(self.call) is Tail:
            return self.call.f(obj,*self.args,**self.kw)
        return self.call(obj,*self.args,**self.kw)
class Tail(object):
    def __init__(self,f):
        self.f = f
    def __call__(self,obj,*args,**kw):
        print "tail:",self.f,obj,args
        ret = self.f (obj, *args,**kw)
        while type(ret) is TailRet:
            ret = ret.handle(obj)
        else:
            return ret

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
            def warp(v,*args,**kw):
                print "warp:",getattr(v,func.__name__)
                return getattr(v,func.__name__)(v,*args,**kw)
            return warp
        return helper
    return matcher
env = {}
matcher = Match(env)
def showMatchEnv():
    print( env )
#__all__ = ["Tail","force","matcher","Match","showMatchEnv"]
__all__ = ["Tail","TailRet","matcher","Match","showMatchEnv"]
