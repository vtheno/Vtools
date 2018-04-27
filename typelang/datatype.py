from util.dt import *
d = Datatype()
c = Constructor()
d.ProcVal() == c.procedure('var','body','env')
# procedure : Var * Exp * Env -> ProcVal
ProcVal = d.ProcVal
procedure = c.procedure
d.ExpVal('a') == c.Num_val('num') \
    | c.Bool_val('bool') \
    | c.Proc_val('proc') 
ExpVal = d.ExpVal
Num_val = c.Num_val # Int -> ExpVal
Bool_val = c.Bool_val # Bool -> ExpVal
Proc_val = c.Proc_val # ProcVal -> ExpVal
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
def expval_proc(e):
    # ExpVal -> ProcVal
    if isinstance(e,Proc_val):
        return e.proc
    raise ExpVal_type_Error("extractor: Proc,{}".format(e))
__all__ = ["ExpVal",
           "Bool_val",
           "Num_val",
           "Proc_val",
           "expval_num","expval_bool","expval_proc",
           "ProcVal","procedure",
       ]


           
