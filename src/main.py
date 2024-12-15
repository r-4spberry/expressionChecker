import my_parser
import lark
from equiv import Equiv
from searchnode import SearchNode
from expressionchecker import ExpressionChecker
import time
from rapidfuzz.distance import Levenshtein


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np







def main():
    
    eq1 = '''
    fraq(
        sum(
            mul(
                var(b),
                var(c),
                var(a)
            ),
            mul(
                var(d),
                var(c),
                udf(lol,num(56), var(a_{1}))                
            ),
            mul(
                pow(var(a),num(7)),
                pow(var(a),num(7)),
                pow(var(a),num(4))
            )
        ),
        var(h)
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
    
    # eq2 = "sum(fraq(mul(var(M_{1}), mul(var(b_{1}), var(T_{1}))), var(W_{1})), fraq(mul(num(-1), mul(var(M_{2}), mul(var(D_{2}), var(T_{2})))), var(W_{2})))"
    
    eq1 = '''
        sum(var(a),var(a))
        '''
    eq2 = '''
    mul(var(a), num(2))
    '''
    
    checker: ExpressionChecker = ExpressionChecker(eq1,eq2,True)
    numIter = 500
    run = checker.search(numIter)
    (s,d,n1,n2) = next(run)
    print("--------------------------------------------------")
    print("equation 1:")
    print(checker.strRepr1)
    print("--------------------------------------------------")
    print("equation 2:")
    print(checker.strRepr2)
    print("--------------------------------------------------")
    print("result: ",s, "similarity: ",d)
    print("--------------------------------------------------")
    print(n1.lineagePretty(8))
    print("--------------------------------------------------")
    print(n2.lineagePretty(8))
    
    print(checker.forest1.forestPretty())
    print(checker.forest2.forestPretty())
    
    print(SearchNode(n1.getGrammarStringRepr()))
    
    # ans = ExpressionChecker.getEqualUpToVariables(checker.forest1,checker.forest2)
    
    # print(ans)
    

if __name__ == "__main__":
    main()
