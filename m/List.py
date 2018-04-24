#coding=utf-8
from dt import *
from Match import *
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
def flip(f):
    return lambda a,b:f(b,a)
def uncurry(f):
    return lambda a,b:f(a)(b)
@Tail
def tail_List(lst,acc):
    if lst == []:
        return acc
    return TailRet(tail_List,lst[1:],Cons(lst[0],acc))
def List(lst):
    lst = list(reversed(lst))
    return tail_List(lst,nil)
@matcher(Nil)
def tail_toPylist(self,acc):
    return acc
@matcher(Cons)
def tail_toPylist(self,acc):
    return TailRet( self.tl.tail_toPylist , [self.hd] + acc )
lst = Cons(1,Cons(2,nil))
print lst
print tail_toPylist(lst,[])
def toPylist(lst):
    return list(reversed(lst.tail_toPylist([])))
#print toPylist(lst)
@matcher(Nil,False)
def null(self):
    return True
@matcher(Cons,False)
def null(self):
    return False
@matcher(Nil,False)
def __eq__(self,a):
    return isinstance(a,Nil)
@matcher(Cons,False)
def __eq__(self,a):
    if isinstance(a,Cons):
        if a.hd == self.hd:
            return self.tl == a.tl
    return False
@Tail
def Helper(lst,acc=[]):
    if lst.null():
        return acc
    return TailRet(Helper,lst.tl,[repr(lst.hd)] + acc )
def helper(lst):
    return reversed(Helper(lst,[]))
@matcher(Nil,False)
def __repr__(self):
    return "[]"
@matcher(Cons,False)
def __repr__(self):
    if  isinstance(self.tl,Nil):
        return "[ {} ]".format(repr(self.hd))
    temp = ",".join(helper(self))
    return "[" + temp + "]"
#print List([1,2,3]) == Cons(1,Cons(2,Cons(3,nil)))
# lst = Cons(1,Cons(2,Cons(3,nil)))
#print lst
#print toPylist(lst)
@matcher(Nil)
def tail_foldl(self,f,acc):
    return acc
@matcher(Cons)
def tail_foldl(self,f,acc):
    TailRet (self.tl.tail_foldl,f,f(acc,self.hd))#self.hd))
def foldl(f,acc,LIST):
    return LIST.tail_foldl(f,acc)
#print lst
#print foldl(lambda a,b:(a,b),"acc",lst)
def foldl1(f,LIST):
    return LIST.tl.tail_foldl(f,LIST.hd)
@matcher(Nil,False)
def rev(self):
    return self
@matcher(Cons,False)
def rev(self):
    return self.tail_foldl(flip(Cons),nil)
def reverse(LIST):
    return LIST.rev()
#print lst.rev(),lst
def foldr(f,end,LIST):
    func = flip(f)
    lst = reverse(LIST)
    return foldl(func,end,lst)
def foldr1(f,end,LIST):
    lst = reverse(LIST)
    func = flip(f)
    return foldl1(func,lst)
#print foldl1(lambda a,b:(a,b),lst)
#print foldr(lambda a,b:(a,b),'end',lst)
@matcher(Nil,False)
def __add__(self,ys):
    return ys
@matcher(Cons,False)
def __add__(self,ys):
    return foldr(Cons,ys,self)
#print lst + lst
def Concat(LIST):
    return foldl(lambda a,b:a+b,nil,LIST)
#print List([lst,lst])
#print Concat(List([lst,lst]))
#print toPylist(lst)
@matcher(Nil)
def tail_map(self,f,acc):
    return acc
@matcher(Cons)
def tail_map(self,f,acc):
    try:
        TailRet( self.tl.tail_map , f,Cons( f (*self.hd) , acc ) )
    except TypeError:
        TailRet( self.tl.tail_map , f ,Cons( f (self.hd) ,acc) )
def Map(f,LIST):
    lst = LIST.rev()
    return lst.tail_map(f,nil)
@matcher(Nil)
def tail_filter(self,f,acc):
    return acc
@matcher(Cons)
def tail_filter(self,f,acc):
    if f(self.hd):
        TailRet(self.tl.tail_filter,f,Cons(self.hd,acc))
    TailRet(self.tl.tail_filter,acc)
lst = List(range(10000))
#print lst
#print toPylist(Map(lambda a : a + 1 ,lst))
#lst = List(range(10000))
#print lst
#print toPylist(lst)
