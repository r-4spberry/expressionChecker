import unittest
from searchnode import SearchNode
from expressionchecker import ExpressionChecker

class TestMatching(unittest.TestCase):
    
    def setUp(self):
        """Initialize reusable objects for tests."""
        pass
    
    def test_withSubstitution(self):
        eq1 = '''
        sum(
            fraq(
                mul(
                    var(l),
                    var(b),
                    var(c)
                ),
                var(kl)          
            ),
            fraq(
                sum(
                    mul(
                        var(d),
                        var(c),
                        var(e)                
                    ),
                    mul(
                        pow(var(l),num(8)),
                        pow(var(l),num(6)),
                        pow(var(l),num(4))
                    )
                ),
                var(kl)
            )
        )
        '''
        eq2 = '''
        sum(
            mul(
                var(a),
                var(b),
                var(c),
                pow(var(h),num(-1))           
            ),
            fraq(
                sum(
                    mul(
                        var(d),
                        var(c),
                        var(e)                
                    ),
                    mul(
                        pow(var(a),num(8)),
                        pow(var(a),num(6)),
                        pow(var(a),num(4))
                    )
                ),
                var(h)
            )
        )
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        self.assertEqual(ans[0],"f")
        ans[2].normalize()
        ans[3].normalize()
        self.assertEqual(ans[2].tree, ans[3].tree)
        
        
    
    def test_withTrailingZeros(self):
        eq1 = '''
        mul(
            mul(
                num(-8),
                num(100),
                var(a)
            ),
            var(k)
        )
        '''
        eq2 = '''
        mul(
            mul(
                num(-800),
                var(a)
            ),
            var(k)
        )
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        self.assertEqual(ans[0],"f")
        ans[2].normalize()
        ans[3].normalize()
        self.assertEqual(ans[2].tree, ans[3].tree)
        
    def test_withSameVarNames(self):
        eq1 = '''
        sum(sum(var(a), var(b)), var(c))
        '''
        eq2 = '''
        sum(sum(var(c), var(d)), var(e))
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        self.assertEqual(ans[0],"f")
        ans[2].normalize()
        ans[3].normalize()
        self.assertEqual(ans[2].tree, ans[3].tree)
        
    def test_multiplyByZero(self):
        eq1 = '''
        mul(sum(var(a), var(b)), var(c), num(0),var(g))
        '''
        eq2 = '''
        num(0)
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")
        
    def test_multiplyByOne(self):
        eq1 = '''
        mul(sum(var(a), var(b)), num(1))
        '''
        eq2 = '''
        sum(var(a), var(b))
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")
    
    def test_addZero(self):
        eq1 = '''
        sum(var(a),var(b),num(0))
        '''
        eq2 = '''
        sum(var(a),var(b))
        '''
        
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")
        
    # def test_addSame(self):
    #     eq1 = '''
    #     sum(var(a),var(a))
    #     '''
    #     eq2 = '''
    #     mul(var(a), num(2))
    #     '''
        
    #     checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
    #     run = checker.search()
    #     ans = next(run)
        
        
    #     ans[2].normalize()
    #     ans[3].normalize()
        
    #     self.assertEqual(ans[2].tree, ans[3].tree)
    #     self.assertEqual(ans[0],"f")
    
    def test_divideNumbers_1(self):
        eq1 = '''
        fraq(
            num(288),
            mul(
                num(8),
                num(3),
                var(g)
            )
        )
        '''
        eq2 = '''
        fraq(
            num(12),
            var(g)
            
        )
        '''
            
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")
        
    def test_divideNumbers_2(self):
        eq1 = '''
        fraq(
            mul(
                num(288),
                var(k)
            ),
            mul(
                num(8),
                num(3),
                var(g)
            )
        )
        '''
        eq2 = '''
        fraq(
            mul(
                num(12),
                var(k)
            ),
            var(g)
            
        )
        '''
            
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")
        
        
    def test_divideNumbers_3(self):
        eq1 = '''
        fraq(
            mul(
                num(288),
                var(k)
            ),
            mul(
                num(8),
                num(3)

            )
        )
        '''
        eq2 = '''
        
            mul(
                num(12),
                var(k)
            )
        
        '''
            
        checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
        run = checker.search()
        ans = next(run)
        
        
        ans[2].normalize()
        ans[3].normalize()
        
        self.assertEqual(ans[2].tree, ans[3].tree)
        self.assertEqual(ans[0],"f")