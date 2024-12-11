import lark
from lark import Tree, Token
from normalize import NormalizeTree
from typing import List



class Equiv:
    "This class is used to produce equivalents of different lark.Trees with our grammar"

    @staticmethod
    def getEquiv(equation: lark.Tree) -> List[lark.Tree]:
        "Function to get equivalents"

        ret: List = []

        if not isinstance(equation, Tree):
            return ret

        ret = ret + Equiv.ruleExpandBrackets(equation)
        ret = ret + Equiv.ruleCombineSum(equation)

        return ret

    @staticmethod
    def ruleExpandBrackets(equation: Tree) -> List[Tree]:
        ret: List = []
        if equation.data == "mul":

            ch: List = []
            ch = equation.children

            # Is there a sum in mul? can we expand brackets?
            sumElem: Tree = None
            others: List[Tree] = []

            for elem in ch:
                if sumElem is None:
                    if elem.data == "sum":
                        sumElem = elem
                    else:
                        others.append(elem)
                else:
                    others.append(elem)

            # There is a sum in mul - expanding brackets
            if sumElem is not None:

                resElem: Tree
                resChildren: list[Tree] = []
                for nom in sumElem.children:
                    resChildren.append(Tree("mul", others + [nom]))
                resElem = Tree("sum", resChildren)
                ret.append(resElem)
                # print(resElem.pretty())
                # print("----debug mul ----")

        return ret
    
    @staticmethod
    def ruleCombineSum(equation: Tree) -> List[Tree]:
        ret:List[Tree] = []
        if equation.data == "sum":
            arr:List[Tree] = []
            for ch in equation.children:
                if ch.data == "sum":
                    arr = arr+ ch.children
                else:
                    arr.append(ch)
            if len(arr) > len(equation.children):
                resElem:Tree = Tree("sum",arr)
                ret.append(resElem)
            elif len(arr) == 1:
                ret.append(arr[0])
                
        
        return ret
            
