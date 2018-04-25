from util import dt
mdt = dt.Datatype()
mcs = dt.Constructor()
mdt.Nat('int') == mcs.Zero() \
                |  mcs.Succ('nat')
Nat = mdt.Nat
Zero = mcs.Zero
Succ = mcs.Succ
zero = Zero()
print( zero ) # => Zero
print( Succ(zero) ) # => Succ [Zero, '...']
from util.Match import *
@matcher(Zero,False) # Zero is class ,False is tail recursion switch 
def toInt(self):
    return 0
@matcher(Succ,False)
def toInt(self):
    # self.nat is before mcs.Succ('nat') 
    return 1 + self.nat.toInt()
one = Succ(zero)
two = Succ(one)
print( toInt(zero) ,toInt(two) ) # => 0 ,2

