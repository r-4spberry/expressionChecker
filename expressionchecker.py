from typing import AnyStr
from typing import List
from searchnode import SearchNode
from collections import defaultdict
from copy import deepcopy
from normalize import NormalizeTree


class ExpressionChecker:
    def __init__(self, str1: AnyStr, str2: AnyStr):
        self.str1 = str1
        self.str2 = str2
        self.dict = defaultdict(list)
        self.forest1: SearchNode = SearchNode(str1)
        self.forest2: SearchNode = SearchNode(str2)
        self.queue1: List[SearchNode] = [self.forest1]
        self.queue2: List[SearchNode] = [self.forest2]
    
    @staticmethod
    def findNodeInSearchSpace(self,node:SearchNode, forestRoot: SearchNode) ->SearchNode:
        ret: SearchNode = None
        if(node == forestRoot):
            return forestRoot
        else:
            for ch in node.childNodes:
                ret = ExpressionChecker.findNodeInSearchSpace(ch)
                if(ret is not None):
                    return ret
        return ret
        
        

    def search(self):
        iteration: int = 0
        close1: SearchNode = None
        close2: SearchNode = None

        while True:
            iteration += 1

            if len(self.queue1) > 0:
                node1: SearchNode = self.queue1.pop(0)
                node1.findChildNodes()
                self.queue1 = self.queue1 + node1.childNodes
                l = len(self.dict[node1.tree])
                if l == 0:
                    self.dict[node1.tree] = [1]
                elif l == 1:
                    if(self.dict[node1.tree][0] == 2):
                        self.dict[node2.tree] = [1,2]
                        yield  ("f",deepcopy(node1), deepcopy(node1))
                elif l == 2:
                    yield  ("f",deepcopy(node1), deepcopy(node1))
                else:
                    pass
                close1 = node1
            
            if len(self.queue2) > 0:
                node2: SearchNode = self.queue2.pop(0)
                node2.findChildNodes()
                self.queue2 = self.queue2 + node2.childNodes
                l = len(self.dict[node2.tree])
                if l == 0:
                    self.dict[node2.tree] = [2]
                elif l == 1:
                    if(self.dict[node2.tree][0] == 1):
                        self.dict[node2.tree] = [1,2]
                        yield ("f",deepcopy(node2), deepcopy(node2))
                elif l == 2:
                    yield ("f",deepcopy(node2), deepcopy(node2))
                else:
                    pass
                close2 = node2
                    
            if len(self.queue1)  == 0 and len(self.queue2)  == 0:
                yield  ("n",close1,close2)

            if iteration % 100 == 0:
                yield ("p",close1, close2)
