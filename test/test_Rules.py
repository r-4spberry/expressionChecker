import unittest
from equiv import Equiv
from my_parser import MyParser
from normalize import NormalizeTree
from lark import Lark
from searchnode import SearchNode


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

    def test_parseNeg(self):
        ans1 = self.parser.parse("num(-1.5)")
        ans2 = self.parser.parse("num(1.5)")
        self.assertNotEqual(ans1,ans2, SearchNode(ans1).__str__() +" " +SearchNode(ans1).__str__())        

