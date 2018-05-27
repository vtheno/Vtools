#coding=utf-8
from .dt import *
from .Match import *
import sys
version = sys.version < '3'
tdt = Datatype()
tcs = Constructor()
tdt.List('a') == tcs.Nil()             \
               | tcs.Cons('hd','tl')
List = tdt.List
Nil = tcs.Nil
nil = Nil()
Cons = tcs.Cons
@matcher(Nil,False)
def null(self):
    return True
@matcher(Cons,False)
def null(self):
    return False

@Tail
def Helper(lst,acc=[]):
    if lst.null():
        return acc
    return Helper(lst.tl,[repr(lst.hd)]+acc)
def helper(lst):
    return reversed(force(Helper(lst,[])))
def toString(self):
    if isinstance(self.tl,Nil):
        return "[ {} ]".format(repr(self.hd))
    temp = ','.join ( helper(self) )
    return "[" + temp + "]"
Cons.__repr__ = toString
@matcher(Nil)
def tail_toPylist(self,acc):
    return acc
@matcher(Cons)
def tail_toPylist(self,acc):
    return self.tl.tail_toPylist ( [self.hd]+acc )
def toPylist(lst):
    return force( reverse(lst).tail_toPylist( [] ) ) 
@Tail
def tail_toList(lst,acc):
    if lst == []:
        return acc
    return tail_toList(lst[1:],Cons(lst[0],acc))
def toList(lst):
    lst = list(reversed(lst))
    return force ( tail_toList(lst,nil) )
@matcher(Nil,True)
def __iter__(self):
    yield self
@matcher(Cons,False)
def __iter__(self):
    yield self.hd
    yield self.tl
class unpack(object):
    """
    usage: 
    with unpack(toList(list(range(9999)))) as (a,(b,_)):
        print a,b
    """
    def __init__(self,v):
        self.v = v
    def __enter__(self):
        return self.v
    def __exit__(self,error_type,value,traceback):
        pass
@matcher(Nil,False)
def __enter__(self):
    return self
@matcher(Cons,False)
def __enter__(self):
    return self
@matcher(Nil,False)
def __exit__(self,*args):
    pass
@matcher(Cons,False)
def __exit__(self,*args):
    pass

@matcher(Nil,False)
def __eq__(self,a):
    if isinstance(a,Nil):
        return True
    return False
@matcher(Cons,False)
def __eq__(self,a):
    if isinstance(a,Cons):
        if a.hd == self.hd:
            return self.tl == a.tl
    return False
def flip(f):
    return lambda a,b: f(b,a)

def uncurry(f):
    return lambda a,b:f(a)(b)

@matcher(Cons)
def tail_foldl(self,f,acc):
    return self.tl.tail_foldl(f,f(acc,self.hd))
@matcher(Nil)
def tail_foldl(self,f,acc):
    return acc
def foldl(f,acc,LIST):
    return force(LIST.tail_foldl(f,acc))
def foldl1(f,LIST):
    return force(LIST.tl.tail_foldl(f,LIST.hd))
"""
@matcher(Nil,False)
def Tfoldr(self,f,end):
    return end
@matcher(Cons,False)
def Tfoldr(self,f,end):
    return f(self.hd,self.tl.Tfoldr(f,end))
"""
def foldr(f,end,LIST):
    " https://wiki.haskell.org/Fold#Overview "
    f2 = flip(f)
    lst = reverse ( LIST )
    return foldl(f2,end,lst)
def foldr1(f,LIST):
    lst = reverse( LIST )
    f2 = flip(f)
    return foldl1(f2,lst)
def Concat(lst):
    return foldl (lambda a,b:a + b,nil,lst)
           
@matcher(Nil)
def rev(self):
    return self
@matcher(Cons)
def rev(self):
    return self.tail_foldl(lambda a,b:Cons(b,a),nil)
def reverse(LIST):
    return force(LIST.rev())

@matcher(Nil,False)
def __add__(self,ys):
    return ys
@matcher(Cons,False)
def __add__(self,ys):
    #print "__add__:",self
    #return reverse ( foldl(lambda b,a:Cons(a,b),reverse(ys),self )
    #return reverse ( foldl(lambda b,a:Cons(a,b),reverse(self),ys) )
    return foldr (Cons,ys,self)

@matcher(Nil)
def tail_map(self,f,acc):
    return acc
@matcher(Cons)
def tail_map(self,f,acc):
    #print "tail_map:",self.hd
    try:
        if version:
            return self.tl.tail_map(f,Cons( apply(f,self.hd) ,acc) )
        else:
            return self.tl.tail_map(f,Cons( f(*self.hd) ,acc) )
    except TypeError:
        return self.tl.tail_map(f,Cons( f(self.hd) ,acc) )
def Map(f,LIST):
    lst = reverse(LIST)
    return force(lst.tail_map(f,nil))
@matcher(Nil)
def tail_filter(self,f,acc):
    return acc
@matcher(Cons)
def tail_filter(self,f,acc):
    if f(self.hd):#apply(f,self.hd):
        return self.tl.tail_filter(f,Cons(self.hd,acc))
    return self.tl.tail_filter(f,acc)
def Filter(f,LIST):
    lst = reverse(LIST)
    return force(lst.tail_filter(f,nil))
@matcher(Nil)
def element(self,obj,acc):
    return acc
@matcher(Cons)
def element(self,obj,acc):
    if self.hd == obj:
        return True
    return self.tl.element(obj,acc)
def elem(obj,lst):
    return force(element(lst,obj,False))

@matcher(Nil)
def tail_length(self,acc):
    return acc
@matcher(Cons)
def tail_length(self,acc):
    return self.tl.tail_length(acc+1)
def length(lst):
    return force ( lst.tail_length (0) )
@Tail
def Tail_Zip(xs,ys,acc):
    if null(xs) or null(ys):
        return acc
    else:
        return Tail_Zip(xs.tl,ys.tl,Cons( (xs.hd,ys.hd) ,acc))
def Zip(xs,ys):
    return force(Tail_Zip(reverse(xs),reverse(ys),nil))
def UnZip(xs):
    x = (nil,nil)
    def f(tup_hd,tup_tl):
        c,b = tup_hd
        cs,bs = tup_tl
        return (Cons(c,cs),Cons(b,bs))
    return foldr(f,x,xs)
__all__ = ["List","Nil","nil","Cons",
           "toPylist",
           "tail_toList","toList",
           "null","flip","uncurry",
           "foldl","foldl1",
           "foldr","foldr1",
           "unpack",
           "Concat","reverse","Zip","UnZip",
           "Map","Filter","elem","length"]
