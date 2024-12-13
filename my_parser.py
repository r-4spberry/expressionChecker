
import lark
from lark import Tree, Token
from normalize import NormalizeTree





class MyParser:
    "This class parses a string with custom grammar into a lark.Tree"
    def __init__(self):

        self.grammar: str = """
        start: expr

        ?expr: term
            | "sum(" expr ("," expr)* ")" -> sum
            | "sub(" expr "," expr ")" -> sub
            | "mul(" expr ("," expr)* ")" -> mul
            | "fraq(" expr "," expr ")" -> fraq
            | "pow(" expr "," expr ")" -> pow
            | "integral(" expr "," expr "," expr ")" -> integral
            | "log(" expr "," expr ")" -> log
            
        ?term: num -> num
            | var -> var

        ?var: "var(" LCASE_LETTER ")"
        
        ?num: "num(" NUMBER ")"
        
        %import common.NUMBER
        %import common.CNAME
        %import common.LCASE_LETTER
        %import common.WS
        %ignore WS
        """

    def parse(self, str_in: str) -> lark.Tree:
        ret: lark.Tree

        parser = lark.Lark(grammar=self.grammar)
        ret = parser.parse(str_in)
        return ret




