#coding=utf-8
from util.Match import *
from parsing import *
__all__ = ["empty_tenv","extend_tenv",
           "apply_tenv","type_of"]
_empty_tenv = "empty-tenv"
_extend_tenv = "extend-tenv"
def empty_tenv():
    return [_empty_tenv]
def extend_tenv(sym,typ,tenv):
    return [_extend_tenv,sym,typ,tenv]
def car(lst): return lst[0]
def cdr(lst): return lst[1:]
def cadr(lst): return car(cdr(lst))
def caddr(lst): return car(cdr(cdr(lst)))
def cadddr(lst): return car(cdr(cdr(cdr(lst))))
class ApplyTenvErr(Exception): pass
@Tail
def tail_apply_tenv(tenv,sym):
    if car(tenv) == _empty_tenv:
        raise ApplyTenvErr("Unbound variable {}".format(sym) )
    elif car(tenv) == _extend_tenv:
        sym1 = cadr(tenv)
        typ  = caddr(tenv)
        saved_tenv = cadddr(tenv)
        if sym == sym1:
            return typ
        else:
            return tail_apply_tenv(saved_tenv,sym)
    else:
        raise ApplyTenvErr("Invaild Env: {}".format(tenv))
def apply_tenv(tenv,sym):
    return force(tail_apply_tenv(tenv,sym))
class TypeNotMatchErr(Exception): pass
def check_equal_type(typ1,typ2,exp1):
    if not typ1 == typ2:
        raise TypeNotMatchErr("{} , {} , {}".format(typ1,typ2,exp1))

@matcher(Const_exp)
def type_of(self,tenv):
    return Int
@matcher(Var_exp)
def type_of(self,tenv):
    return apply_tenv(tenv,self.var)
@matcher(Diff_exp)
def type_of(self,tenv):
    ty1 = force( type_of(self.exp1,tenv) )
    ty2 = force( type_of(self.exp2,tenv) )
    check_equal_type(ty1,Int,self.exp1)
    check_equal_type(ty2,Int,self.exp2)
    return Int
@matcher(Zerop_exp)
def type_of(self,tenv):
    ty1 = force( type_of(self.exp,tenv) )
    check_equal_type(ty1,Int,self.exp)
    return Bool
@matcher(If_exp)
def type_of(self,tenv):
    ty1 = force( type_of(self.exp1,tenv) )
    ty2 = force( type_of(self.exp2,tenv) )
    ty3 = force( type_of(self.exp3,tenv) )
    check_equal_type(ty1,Bool,self.exp1)
    check_equal_type(ty2,ty3,self.exp2)
    return ty2
@matcher(Let_exp)
def type_of(self,tenv):
    exp1_typ = force( type_of(self.exp1,tenv) )
    return type_of(self.body,extend_tenv(self.var,exp1_typ,tenv))
@matcher(Proc_exp)
def type_of(self,tenv):
    # self.var_type
    result_type = force( 
        type_of(self.body,extend_tenv(self.var,self.var_type,tenv))
        )
    return Proc_Type(self.var_type,result_type)
class TypeOfErr(Exception):pass
@matcher(Call_exp)
def type_of(self,tenv):
    #print "call:",tenv
    exp1_typ = force( type_of(self.exp1,tenv) ) # : Proc_Type
    exp2_typ = force( type_of(self.exp2,tenv) ) # : Type
    if isinstance(exp1_typ,Proc_Type):
        argtyp = exp1_typ.argtype
        result_typ = exp1_typ.result_type
        check_equal_type(argtyp,exp2_typ,self.exp2)
        return result_typ
    raise TypeOfErr("rator not a proc type: {},{}".format(exp1_typ,exp2_typ))
@matcher(Letrec_exp)
def type_of(self,tenv):
    # self.bvar self.proc_body self.letrec_body
    arg_type = self.parg_type
    result_type = self.prest_type
    tenv_for_letrec_body = extend_tenv(self.proc_name,
                                      Proc_Type(arg_type,result_type),
                                      tenv)
    #print "tenv_for_letrec_body:",tenv_for_letrec_body
    proc_body_type = force(type_of(self.proc_body,
                                   extend_tenv(self.bvar,arg_type,
                                               tenv_for_letrec_body)) )
    check_equal_type(proc_body_type,result_type,self.proc_body)
    return type_of(self.letrec_body,tenv_for_letrec_body)

                                      
#print Bool == Bool
#print Int == Int
#print Int == Bool                 
