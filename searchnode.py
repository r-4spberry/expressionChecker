from typing import List
from my_parser import MyParser
from copy import deepcopy
from lark import Tree
from equiv import Equiv
from copy import deepcopy
from normalize import NormalizeTree


class SearchNode:
    def __init__(self, equation_or_ancestor):
        parser: MyParser = MyParser()
        if isinstance(equation_or_ancestor, str):
            self.tree: Tree = parser.parse(equation_or_ancestor).children[0]
        elif isinstance(equation_or_ancestor, SearchNode):
            self.tree: Tree = deepcopy(equation_or_ancestor.tree)
        else:
            raise TypeError("Expected a string or a Tree")
        self.normalize()
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
        arr = arr + [curTree]
        if isinstance(curTree, Tree):
            for child in curTree.children:
                arr = arr + self.getElementsReferences(child)
        return arr

    def getChildNodes(self) -> List:
        """computes all possible equivalents of a tree and returns them in a list.
        DOES NOT ADD them to childNodes of a node"""
        ret: List[SearchNode] = []
        for numRef in range(len(self.elemRefs)):
            for numEq in range(len(self.elemEquivs[numRef])):
                nextChild: SearchNode = SearchNode(self)
                nextChild.elemRefs[numRef].data = self.elemEquivs[numRef][numEq].data
                nextChild.elemRefs[numRef].children = deepcopy(
                    self.elemEquivs[numRef][numEq].children
                )
                ret.append(nextChild)
        for i in ret:
            i.normalize()
        return ret

    def findChildNodes(self) -> None:
        "computes all possible equivalents of a tree. adds them to childNodes of a node"
        self.childNodes = self.getChildNodes()

    def setAncestor(self, ancestor):
        if not isinstance(ancestor, SearchNode):
            raise TypeError("Expected SearchNode")
        self.ancestorNode = ancestor

    def normalize(self):
        normalizer: NormalizeTree = NormalizeTree()
        self.tree = normalizer.transform(self.tree)
