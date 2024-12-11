from typing import List
from my_parser import MyParser
from copy import deepcopy
from lark import Tree
from equiv import Equiv
from copy import deepcopy


class SearchNode:
    def __init__(self, equation_or_ancestor):
        parser:MyParser = MyParser()
        if isinstance(equation_or_ancestor, str):
            self.tree: Tree = parser.parse(equation_or_ancestor).children[0]
        elif isinstance(equation_or_ancestor, SearchNode):
            self.tree: Tree = deepcopy(equation_or_ancestor.tree)
        else:
            raise TypeError("Expected a string or a Tree")
        self.elemRefs: List[Tree] = self.getElementsReferences(self.tree)
        self.elemEquivs: List[Tree] = self.getAllElemEquivalents(self.elemRefs)
        self.childNodes: List[SearchNode] = []
        self.ancestorNode = None

    def getAllElemEquivalents(self, arr: List[Tree]) -> List[Tree]:
        ret: List[Tree] = []
        for ref in self.elemRefs:
            ret.append(Equiv.getEquiv(ref))

        return ret

    def getElementsReferences(self, curTree: Tree) -> List[Tree]:
        arr = []
        arr = arr+ [curTree]
        if(isinstance(curTree,Tree)):
            for child in curTree.children:
                arr = arr + self.getElementsReferences(child)
        return arr

    def getChildNodes(self) -> List:
        ret: List[SearchNode] = []
        for numRef in range(len(self.elemRefs)):
            for numEq in range(len(self.elemEquivs[numRef])):
                nextChild: SearchNode = SearchNode(self)
                nextChild.elemRefs[numRef].data = self.elemEquivs[numRef][numEq].data
                nextChild.elemRefs[numRef].children = deepcopy(self.elemEquivs[numRef][numEq].children)
                ret.append(nextChild)
        return ret
    
    def findChildNodes(self) ->None:
        self.childNodes = self.getChildNodes()
