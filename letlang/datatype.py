from util.dt import *
d = Datatype()
c = Constructor()
d.ExpVal('a') == c.Num_val('num') \
    | c.Bool_val('bool') 
ExpVal = d.ExpVal
Num_val = c.Num_val # Int -> ExpVal
Bool_val = c.Bool_val # Bool -> ExpVal
class ExpVal_type_Error(Exception): pass
def expval_num(e):
    # ExpVal -> Int
    if isinstance(e,Num_val):
        return e.num
    raise ExpVal_type_Error("extractor: Num,{}".format(e))
def expval_bool(e):
    # ExpVal -> Bool
    if isinstance(e,Bool_val):
        return e.bool
    raise ExpVal_type_Error("extractor: Bool,{}".format(e))
__all__ = ["ExpVal",
           "Bool_val",
           "Num_val",
           "expval_num","expval_bool",
       ]


           
