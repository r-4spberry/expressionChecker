import unittest
from equiv import Equiv
from my_parser import MyParser
from normalize import NormalizeTree
from lark import Lark,Tree
from searchnode import SearchNode
from typing import List


class TestEquiv(unittest.TestCase):
    
    def setUp(self):
        """Initialize reusable objects for tests."""
        self.parser = MyParser()
        self.normalizer = NormalizeTree()
    
    def test_ruleCombineSum(self):
        
        before: str = "sum(sum(num(-1),var(b)),var(c))"
        after: str = "sum(num(-1),var(b),var(c))"
        
        treeBefore = self.parser.parse(before).children[0]
        treeAfter = self.normalizer.transform(self.parser.parse(after).children[0])
        
        ans = Equiv.ruleCombineSum(treeBefore)
        for i in range(len(ans)):
            ans[i] = self.normalizer.transform(ans[i])
        
        self.assertEqual(treeAfter,ans[0])
        
        
    def test_ruleCombineMul(self):
        
        before: str = "mul(mul(var(a),var(b)),var(c))"
        after: str = "mul(var(a),var(b),var(c))"
        
        treeBefore = self.parser.parse(before).children[0]
        treeAfter = self.normalizer.transform(self.parser.parse(after).children[0])
        
        ans = Equiv.ruleCombineMul(treeBefore)
        for i in range(len(ans)):
            ans[i] = self.normalizer.transform(ans[i])
        
        self.assertEqual(treeAfter,ans[0])
        
    def test_ruleinvertFraq(self):
        
        before: str = "fraq(num(-1),var(b))"
        after: str = "mul(num(-1),pow(var(b),num(-1)))"
        
        treeBefore = self.parser.parse(before).children[0]
        treeAfter = self.normalizer.transform(self.parser.parse(after).children[0])
        
        ans = Equiv.ruleInvertFraq(treeBefore)
        bef = SearchNode(treeBefore)
        aft = SearchNode(ans[0])
        for i in range(len(ans)):
            ans[i] = self.normalizer.transform(ans[i])
        
        self.assertEqual(treeAfter,ans[0],SearchNode(treeAfter).__str__() +" " +SearchNode(ans[0]).__str__())
        
    def test_ruleMutiplyAllNumbers(self):
        
        before: str = "mul(var(a), num(-10), num(500.5), num(-98), var(b))"
        after: str = "mul(var(a),var(b),num(490490.0))"
        
        tB,tE,arr = TestEquiv.runRule(before,after,Equiv.ruleMutiplyAllNumbers)
        
        self.assertEqual(tE,arr[0])
        
    def test_ruleCombinePowers(self):
        before: str = "mul(sum(var(a),var(b)),pow(var(b),num(6)),pow(var(b),sum(var(a),var(b))),pow(var(a),var(b)))"
        after: str = "mul(sum(var(a),var(b)), pow(var(b),sum(num(6), sum(var(a),var(b)))), pow(var(a),var(b)))"
        
        tB,tE,arr = TestEquiv.runRule(before,after,Equiv.ruleCombinePowers)
        
        self.assertEqual(tE,arr[0],SearchNode(tE).__str__() + " " + SearchNode(arr[0]).__str__())
        
        

    def test_parseNeg(self):
        ans1 = self.parser.parse("num(-1.5)")
        ans2 = self.parser.parse("num(1.5)")
        self.assertNotEqual(ans1,ans2, SearchNode(ans1).__str__() +" " +SearchNode(ans1).__str__())        
        
    @staticmethod
    def runRule(equation:str, expected:str,rule:callable):
        parser:MyParser = MyParser()
        normalizer:NormalizeTree = NormalizeTree()
        treeBefore = parser.parse(equation).children[0]
        treeExpected = normalizer.transform(parser.parse(expected).children[0])
        
        eqArray:List[Tree] = rule(treeBefore)
        
        
        treeBefore = normalizer.transform(treeBefore)
        treeExpected = normalizer.transform(treeExpected)
        for i in range(len(eqArray)):
            eqArray[i] = normalizer.transform(eqArray[i])
        return(treeBefore, treeExpected,eqArray)

