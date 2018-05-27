#coding=utf-8
from Letlang import *

print( read(expr)("cons 1 cons 2 cons 3 nil").value_of(empty_env()) )
print( read(expr)("car cons 1 cons 2 cons 3 nil").value_of(empty_env()) )
print( read(expr)("cdr cons 1 cons 2 cons 3 nil").value_of(empty_env()) )
print( read(expr)("null? cons 1 cons 2 cons 3 nil").value_of(empty_env()) )
t =  read(expr)("""
let a = cons 1 cons 2 nil 
in unpack a,b = a 
       in  -( minus(a) b ) 
""").value_of(empty_env())
print( t )
#print( exp_cons2Cons(t) )

print( read(expr)("proc (x) x").value_of(empty) )
print( read(expr)("( proc (x) -(x minus(x)) 6)").value_of(empty) )
print( read(expr)("""
let f = proc (x) -(x 11)
in (f (f 77))
""").value_of(empty) )
print( read(expr)("""
let x = 200
in let f = proc(z) -(z x)
   in let x = 100
      in let g = proc(z) -(z x)
         in -( (f 1) (g 1) )
""").value_of(empty) )
print( read(expr)("""
let makemult = proc (maker) 
                  proc (x)
                     if zero? x 
                     then 0
                     else -( ( (maker maker) -(x 1) ) minus(4))
in let times4 = proc(x) ((makemult makemult) x)
   in (times4 3)
""").value_of(empty) )
print( read(expr)("""
let a = 5
in  let p = proc (x) -(x a)
        a = 5
    in  -(a (p 2))
""").value_of(empty) )
