from .List import *
from .Match import *
class GetIdentErr(Exception):pass
class GetNextTokenErr(Exception):pass
@matcher(Nil)
def tail_Get(self,x,acc):
    return acc
@matcher(Cons)
def tail_Get(self,x,acc):
    with unpack(self.hd) as (t,c):
        if x == t:
            return c
        return self.tl.tail_Get(x,acc)
def Get(x,lst):
    return force(lst.tail_Get(x,nil))

class Lexical(object):
    def __init__(self,SpecTab):
        self.SpecTab = SpecTab
    def IsDigit(self,s):
        # IsDigit : str -> bool
        return "0" <= s <= "9"
    def IsLetter(self,s):
        # IsLetter : str -> bool
        return "a" <= s <= "z" or "A" <= s <= "Z"
    def IsSeparator(self,s):
        # IsSeparator : str -> bool
        return s == " " or s == "\n" or s == "\t"
    def explode(self,string):
        # explode : string -> str list 
        return toList(string)
    def implode(self,LIST):
        # implode : str list -> string
        return "".join(toPylist(LIST))
    @Tail
    def Tail_GetNumAux(self,buf,lst):
        if lst.null() :
            return (self.implode( reverse(buf)  ),nil)
        else:
            with lst as (x,xs):
                if self.IsDigit(x):
                    return self.GetNumAux ( Cons(x,buf),xs)
                else:
                    return (self.implode( reverse(buf) ),lst)
    def GetNum(self,lst):
        return force( self.Tail_GetNumAux(nil,lst) )
    @Tail
    def Tail_GetIdentAux(self,buf,lst):
        if lst.null() :
            return self.implode( reverse(buf) ),nil
        else:
            with lst as (x,xs):
                if self.IsLetter(x) or self.IsDigit(x):
                    return self.Tail_GetIdentAux( Cons(x,buf) ,xs)
                else:
                    return self.implode ( reverse(buf) ),lst
    def GetIdent(self,lst):
        with lst as (x,xs):
            if self.IsLetter(x) or self.IsDigit(x):
                return force(self.Tail_GetIdentAux(Cons(x,nil),xs))
            else:
                raise GetIdentErr("GetIdentErr")
    def GetTail(self,p,buf,lst):
        if lst.null():
            return self.implode( reverse(buf)),nil
        else:
            with lst as (x,xs):
                if p(x):
                    return self.GetTail(p,Cons(x,buf),xs)
                else:
                    return self.implode( reverse(buf) ),lst
    @Tail
    def Tail_GetTail(self,p,buf,lst):
        if lst.null():
            return self.implode( reverse(buf)),nil
        else:
            with lst as (x,xs):
                if p(x):
                    return self.Tail_GetTail(p,Cons(x,buf),xs)
                else:
                    return self.implode( reverse(buf) ),lst
    @Tail
    def Tail_GetSymbol(self,spectab,tok,lst):
        if lst.null():
            return tok,nil
        else:
            with lst as (x,xs):
                if elem(x,Get(tok,spectab)):
                    return self.Tail_GetSymbol(spectab,tok + x ,xs)
                else:
                    return tok,lst
    def GetSymbol(self,spectab,tok,lst):
        return force(self.Tail_GetSymbol(spectab,tok,lst))
    def GetNextToken(self,spectab,lst):
        if lst.null():
            raise GetNextTokenErr("GetNextTokenErr: {}".format(lst))
        else:
            with lst as (x,xs):
                if isinstance(xs,Nil):
                    return x,nil
                else:
                    with xs as (c,cs):
                        if self.IsLetter(x):
                            return self.GetTail(lambda x:self.IsLetter(x) or self.IsDigit(x),Cons(x,nil),xs)
                        elif self.IsDigit(x):
                            return self.GetTail(self.IsDigit,Cons(x,nil),xs)
                        elif elem(c,Get(x,spectab)):
                            return self.GetSymbol(spectab,self.implode(toList([x,c])),cs)
                        else:
                            return (x,xs)
    @Tail
    def Tail_Tokenise(self,spectab,lst,acc):
        if lst.null():
            return acc
        else:
            with lst as (x,xs):
                if self.IsSeparator(x):
                    return self.Tail_Tokenise(spectab,xs,acc)
                else:
                    with unpack(self.GetNextToken(spectab,lst)) as (t,ts):
                        return self.Tail_Tokenise(spectab,ts,Cons(t,acc))
    def Tokenise(self,spectab,lst):
        return reverse( force(self.Tail_Tokenise(spectab,lst,nil)) )
    def Lex(self,string):
        return self.Tokenise(self.SpecTab,self.explode(string))
def test():
    tab = toList([ ("=",toList([">","<","="]))] )
    Lex = Lexical( tab )
    string = "66666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666666"
    #print len(Lex.GetNum(toList(string))[0]) == len(string)
    print( Lex.GetIdent(toList("abc123")) )
    print( Get("=",tab) )
    print( Lex.GetSymbol(Lex.SpecTab,"=",toList(">")) )
    print( Lex.GetNextToken(Lex.SpecTab,toList("abcd 666 =>")) )
    print( Lex.Tokenise(Lex.SpecTab,toList("abc 666 =>")) )
    print( Lex.Lex("a => bc1") )
    print( Lex.Lex(string) )

__all__ = ["Lexical"]
