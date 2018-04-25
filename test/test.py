from util.Parsec import *
number = token(nat)
print(read(number)(input(">> ")))
