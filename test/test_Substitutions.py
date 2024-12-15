import unittest
from searchnode import SearchNode
from expressionchecker import ExpressionChecker

class TestSubstitutions(unittest.TestCase):
    
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
        
        checker: ExpressionChecker = ExpressionChecker()