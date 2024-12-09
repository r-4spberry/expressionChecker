import lark
class my_parser:
    def __init__(self):
        self.grammar : str = '''
    start: expr

    ?expr: term
         |  expr "+" expr    -> add
         |  expr "-" expr   -> sub
         |  expr "/" expr   -> div
         |  expr "*" expr   -> mul
         | "(" expr ")"
         | function
         
         
    ?term: NUMBER -> number
         | variable -> var

    ?function: "sum(" expr "," expr ")" ->sumfun
             | "integral(" expr "," expr "," expr ")" -> integralfun

    ?variable: "var(" LCASE_LETTER ")"
    
    %import common.NUMBER
    %import common.CNAME
    %import common.LCASE_LETTER
    %import common.WS
    %ignore WS
    '''
    
    def parse(self, str_in:str)->lark.Tree: 
        ret : lark.Tree
        
        parser = lark.Lark(grammar=self.grammar)
        ret = parser.parse(str_in)
        return ret