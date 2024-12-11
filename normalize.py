import lark
from lark import Tree, Token


class NormalizeTree(lark.Transformer):
    "This class normalizes a lark.Tree"
    def sum(self, children):
        s = sorted(children, key=str)
        return lark.Tree("sum", s)

    def mul(self, children):
        s = sorted(children, key=str)
        return lark.Tree("mul", s)