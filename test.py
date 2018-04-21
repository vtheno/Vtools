#coding=utf-8
from dt import *
dt = Datatype()
c = Constructor()
dt.program('a') == c.pgm('exp')
program = dt.program
a_program = c.pgm
is_program = lambda x:isinstance(x,program)
pg = a_program('a')
print ( pg )
print (pg.exp,pg.index)
