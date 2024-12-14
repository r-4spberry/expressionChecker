from typing import AnyStr
from typing import List
from typing import Dict
from typing import Tuple
from searchnode import SearchNode
from collections import defaultdict
from copy import deepcopy
from normalize import NormalizeTree
import heapq
from metrics import Metrics
from lark import Tree


class ExpressionChecker:
    def __init__(self, str1: AnyStr, str2: AnyStr):
        self.heap: List[ExpressionChecker.heapEntry] = []
        "used to store pair of equations and a metric associated with them"
        heapq.heapify(self.heap)

        self.eqMap: Dict[Tree, ExpressionChecker.mapEntry] = dict()
        "used to store representations of trees and if they were found from each root"

        self.initial_str1: str = str1
        self.initial_str2: str = str2

        self.forest1: SearchNode = SearchNode(self.initial_str1)
        self.forest2: SearchNode = SearchNode(self.initial_str2)

        # self.addEqToMap(self.forest1, 1)
        # self.addEqToMap(self.forest2, 2)

        self.strRepr1: str = self.forest1.__str__()
        self.strRepr2: str = self.forest2.__str__()

        self.addToHeap(self.forest1, self.forest2)

        self.lowestMetric: int = self.heap[0].metricValue
        self.close1: SearchNode = self.heap[0].node1
        self.close2: SearchNode = self.heap[0].node2

        self.foundEquivalent = False

    class mapEntry:
        def __init__(self, repr: str):
            self.repr: str = repr
            self.node1: SearchNode = None
            self.node2: SearchNode = None
            
        def __repr__(self):
            ret = "("
            ret = ret + self.repr
            if self.node1 is not None:
                ret = ret +" node1"
            else:
                ret = ret + "  None"
                
            if self.node2 is not None:
                ret = ret +" node2"
            else:
                ret = ret + "  None"
            ret = ret +")"
            return ret

    class heapEntry:
        def __init__(self, eq1: SearchNode, eq2: SearchNode, metric: int):
            self.metricValue:int = metric
            self.node1: SearchNode = eq1
            self.node2: SearchNode = eq2
            
        def __lt__(self, other):
            return self.metricValue < other.metricValue

        def __eq__(self, other):
            return self.metricValue == other.metricValue
        
        def __repr__(self):
            ret = "("
            ret = ret + str(self.metricValue)
            ret = ret + " "
            ret = ret + self.node1.__str__()
            ret = ret + " "
            ret = ret + self.node2.__str__()
            ret = ret + ")"
            return ret

    def addToHeap(
        self,
        eq1: SearchNode,
        eq2: SearchNode,
        metric: callable = Metrics.levenshteinMetric,
    ) -> None:
        streq1: str = ""
        streq2: str = ""

        if eq1 in self.eqMap:
            streq1 = self.eqMap[eq1].repr
        else:
            streq1 = eq1.__str__()

        if eq2 in self.eqMap:
            streq2 = self.eqMap[eq2].repr
        else:
            streq2 = eq2.__str__()

        metricValue: int = metric(self.strRepr1, streq1, streq2, self.strRepr2)
        value: ExpressionChecker.heapEntry = ExpressionChecker.heapEntry(eq1, eq2,metricValue)
        heapq.heappush(self.heap, value)

    def getPairWithLowestMetric(self) -> "ExpressionChecker.heapEntry":
        try:
            ret: ExpressionChecker.heapEntry = heapq.heappop(self.heap)
        except IndexError as e:
            ret: ExpressionChecker.heapEntry =    ExpressionChecker.heapEntry(None, None, 99999999999)
            
        return ret

    def addEqToMap(self, eq: SearchNode, first_or_second: int) -> None:
        if eq.tree not in self.eqMap:
            self.eqMap[eq.tree] = ExpressionChecker.mapEntry(eq.__str__())

        if first_or_second == 1:
            self.eqMap[eq.tree].node1 = eq
        elif first_or_second == 2:
            self.eqMap[eq.tree].node2 = eq

    def search(self, numIter: int = 100):
        iteration: int = 1

        while True:

            if self.foundEquivalent:
                yield ("f", self.close1, self.close2)
                continue

            if iteration % numIter == 0:
                yield ("p", self.close1, self.close2)
                continue

            
            heapEntry = self.getPairWithLowestMetric()
            

            if (heapEntry.node1 is None) and (heapEntry.node2 is None):
                yield ("n", self.close1, self.close2)
                continue

            if heapEntry.metricValue < self.lowestMetric:
                self.close1 = heapEntry.node1
                self.close2 = heapEntry.node2
                self.lowestMetric = heapEntry.metricValue

            exp1: bool = False
            exp2: bool = False
            
            # expanding all children of node1
            if not heapEntry.node1.expanded:
                exp1 = True
                n = heapEntry.node1
                if (n.tree not in self.eqMap) or (self.eqMap[n.tree].node1 is None):
                    n.findChildNodes()
                
            # expanding all children of node2
            if not heapEntry.node2.expanded:
                exp2 = True
                n = heapEntry.node2
                if (n.tree not in self.eqMap) or (self.eqMap[n.tree].node2 is None):         
                    n.findChildNodes()
            
            # adding node1 to map
            self.addEqToMap(heapEntry.node1,1)
            
            # adding node2 to map
            self.addEqToMap(heapEntry.node2,2)
                    
            # updating the heap with node1
            if not heapEntry.node1.expanded:
                for ch1 in heapEntry.node1.childNodes:
                    for k in self.eqMap:
                        if self.eqMap[k].node2 is not None:
                            self.addToHeap(ch1,self.eqMap[k].node2)
                        
            # updating the heap with node2
            if not heapEntry.node2.expanded:
                for ch2 in heapEntry.node2.childNodes:
                    for k in self.eqMap:
                        if self.eqMap[k].node1 is not None:
                            self.addToHeap(self.eqMap[k].node1,ch2)
                        
            # marking both nodes expanded
            heapEntry.node1.expanded = True
            heapEntry.node2.expanded = True
            
            
                
            
                
            
            
            if exp1 or exp2:
                iteration+=1
            
            # checking if we found an equivalence
            if heapEntry.node1 is not None and (heapEntry.node1.tree in self.eqMap):
                mapEntry: ExpressionChecker.mapEntry = self.eqMap[heapEntry.node1.tree]
                if (mapEntry.node1 is not None) and (mapEntry.node2 is not None):
                    self.close1 = mapEntry.node1
                    self.close2 = mapEntry.node2
                    self.foundEquivalent = True
                    continue
            
            if heapEntry.node1 is not None and (heapEntry.node1.tree in self.eqMap):
                mapEntry: ExpressionChecker.mapEntry = self.eqMap[heapEntry.node2.tree]
                if (mapEntry.node1 is not None) and (mapEntry.node2 is not None):
                    self.close1 = mapEntry.node1
                    self.close2 = mapEntry.node2
                    self.foundEquivalent = True
                    continue
