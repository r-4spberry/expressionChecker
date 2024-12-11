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
        ch :List = []
        
        normalizer: NormalizeTree = NormalizeTree()
        
        for elem in equation.children:
            ch.append(normalizer.transform(elem))
            
        if equation.data == "mul":
            
            # Is there a sum in mul? can we expand brackets?
            sumElem :Tree = None
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
                    resChildren.append(Tree("mul",others + [nom]))
                resElem = Tree("sum",resChildren)
                ret.append(resElem)
                        
                        
                        
            
            
        
        return ret
