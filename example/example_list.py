from util.List import *
print( dir() )

lst = list(range(9999))
hd,*tl = lst
print( hd )
print( tl )
del hd,tl
Lst = toList(lst)
try:
    print( hd,tl )
except NameError as e:
    with Lst as (hd,tl):
        print( hd )
        print( tl )
        print( type(hd),type(tl) )
        print( Lst.hd is hd )
        print( Lst.tl is tl )
    del hd,tl
del lst,Lst
lst = Cons(1,Cons(2,Cons(3,Cons(4,nil))))
print( lst,type(lst) )
Lst = toPylist(lst)
print( Lst,type(Lst) )
with lst as (a,(b,c)):
    print (a,b,c)
    print (a is lst.hd)
    print (b is lst.tl.hd)
    print (c is lst.tl.tl)


