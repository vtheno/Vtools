#coding=utf-8
from dt import *
from Match import *
tdt = Datatype()
tcs = Constructor()
tdt.List('a') == tcs.Nil()             \
               | tcs.Cons('hd','tl')
List = tdt.List
Nil = tcs.Nil
nil = Nil()
Cons = tcs.Cons

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

@matcher(Nil,False)
def null(self):
    return True
@matcher(Cons,False)
def null(self):
    return False

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
        return self.tl.tail_map(f,Cons( apply(f,self.hd) ,acc) )
    except:
        return self.tl.tail_map(f,Cons( f(*self.hd) ,acc) )
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

