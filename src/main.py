import my_parser
import lark
from equiv import Equiv
from searchnode import SearchNode
from expressionchecker import ExpressionChecker


def main():
    
    eq1 = '''
        sum(
            mul(
                var(a),
                num(3),
                num(9)
            ),
            mul(
                pow(var(a), num(2)),
                pow(var(a), var(g))                
            ),
            fraq(
                sum(
                    var(a), 
                    var(b)
                ),
                var(c)
            )            
        )
    '''
    
    eq2 = "var(a)"
    
    
    
    checker: ExpressionChecker = ExpressionChecker(eq1,eq2)
    run = checker.search()
    
    ans = next(run)
    
    print("-------------------------------------------------------")
    print("res:")
    print(ans[0])
    print(ans[1])
    print(ans[2])
    print("-------------------------------------------------------")
    print("forest1:")
    print(checker.forest1.forestPretty(depth = 3))
    print("-------------------------------------------------------")
    print("forest2:")
    print(checker.forest2.forestPretty(depth = 3))
    print("-------------------------------------------------------")
    
    
    

if __name__ == "__main__":
    main()
