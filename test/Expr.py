#coding=utf-8
"http://matt.might.net/articles/discrete-math-and-code/"
"""
E ::= e + e 
    | e * e
    | n
eval(e+e) = eval(e) + eval(e)
eval(e*e) = eval(e) * eval(e)
eval(n)   = n
"""
class Exp:
    @staticmethod
    def eval():
        raise NotImplementedError
class Sum(Exp):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def eval(cls):
        return cls.left.eval() + cls.right.eval()
class Product(Exp):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def eval(cls):
        return cls.left.eval() * cls.right.eval()
class Const(Exp):
    def __init__(self,value):
        self.value = value
    def eval(cls):
        return cls.value
a = Sum(Const(1),Const(2))
print a.eval()
"""
datatype Exp = Const of int
             | Sum of Exp * Exp
             | Product of Exp * Exp
fun eval (Const n) = n
  | eval (Sum (a,b)) = eval a + eval b
  | eval (Product (a,b)) = eval a * eval b
"""

"""
x = foldr (+) 0 [1,2,3]
head = foldr const undefined
tail x = let Just (_,t) = foldr tailHelper Nothing x in t 
  where 
    tailHelper x Nothing = Just (x,[])
    tailHelper x (Just (y,z)) = Just (x,y:z)
nil a b = b
cons h t a b = a h (t a b)
y = cons 1 (cons 2 (cons 3 nil))
z = y (:) []

"""
def foldr(f,end,l):
    if l==[]:
        return end
    else:
        return f(l[0],foldr(f,end,l[1:]))
print foldr(lambda x,y:x+y,0,[1,2,3])
def nil(a,b):
    return b
def cons(h,t):
    def _cons(a,b):
        return a(h,t(a,b))
    return _cons
l = cons(1,cons(2,cons(3,nil)))
print l(lambda x,y:x+y,0)
print l(lambda x,y:[x]+y,[])

"""
data Expr = X | Const Int | Binop (Int -> Int -> Int) Expr Expr

> efold :: a -> (Int -> a) -> ((Int -> Int -> Int) -> a -> a -> a) -> Expr -> a
> efold x _ _ X = x
> efold _ c _ (Const a) = c a
> efold x c b (Binop f lt rt) = b f (efold x c b lt) (efold x c b rt)

E:\Parsec\go\img_sex\A Neighborhood of Infinity  Purely functional recursive types in Haskell and Python.htm
"""
