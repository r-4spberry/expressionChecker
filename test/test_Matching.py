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