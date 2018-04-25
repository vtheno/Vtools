from util.Match import Tail,force
class unpack(object):
    def __init__(self,v):
        self.v = v
    def __enter__(self):
        return _f(self.v)
    def __exit__(self,*args):
        pass
@Tail
def f(lst,acc):
    if lst == []:
        return acc
    return f(lst[1:],[lst[0],acc])
def _f(lst):
    lst = list(reversed(lst))
    return force(f(lst,[]))
lst = list(range(6)) # 6 or more 
print( _f(lst) )
with unpack(lst) as (x,xs):
    print( x )
    print( xs )
