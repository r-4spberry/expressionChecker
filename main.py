import my_parser
import lark
from equiv import Equiv
from searchnode import SearchNode
from expressionchecker import ExpressionChecker


def main():



    equation = \
        "mul( \
            var(a),\
            var(e),\
            var(c),\
            var(c),\
            num(888),\
            sum(\
                var(g),\
                num(77),\
                fraq(\
                    num(888),\
                    num(999)\
                ),\
                mul(\
                    sum(\
                        num(221),\
                        var(a)\
                    ),\
                    var(b)\
                )\
            )\
        )"
    

    eq1: str = "sum(\
            mul(var(a),var(b)),\
            mul(var(b),var(c)),\
            mul(var(d),sum(var(c),var(e)))\
            \
            \
            \
            \
            \
        )"
    eq2: str = "sum(\
            mul(var(b),sum(var(a),var(c))),\
            mul(var(c),var(d)),\
            mul(var(d),var(e))\
            \
            \
            \
            \
            \
        )"

    # eq2: str = "sum(var(a),num(7))"
    
    print("before")
    print("--------------------------------------------")
    print(SearchNode(eq1))
    print("--------------------------------------------")
    print(SearchNode(eq2))
    print("--------------------------------------------")

    checker: ExpressionChecker = ExpressionChecker(eq1,eq2)
    search = checker.search()
    ans = next(search)
    print("after")
    print(ans[0])
    print("--------------------------------------------")
    print(ans[1])
    print("--------------------------------------------")
    print(ans[2])
    

if __name__ == "__main__":
    main()
