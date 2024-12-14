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
    
    eq2 = '''
        mul(
            sum(
                mul(
                    var(a),
                    num(3),
                    num(9)
                ),
                mul(
                    pow(var(a), num(2)),
                    pow(var(a), var(g))     
                )
                ,
                fraq(
                    var(g),
                    num(288)
                )
            ),
            num(431)
        )
    '''
    
    
    
    checker: ExpressionChecker = ExpressionChecker(eq1,eq2)
    
    numIter = 10
    run = checker.search(numIter)
    start_time = time.time()
    
    ans = next(run)
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Iterations: ",numIter," Time: ", elapsed_time)
    print(ans)
    
    # print("-------------------------------------------------------")
    # print("res:")
    # print(ans[0])
    # print(ans[1])
    # print(ans[2])
    # print("-------------------------------------------------------")
    # print("forest1:")
    # print(checker.forest1.forestPretty(depth = 3))
    # print("-------------------------------------------------------")
    # print("forest2:")
    # print(checker.forest2.forestPretty(depth = 3))
    # print("-------------------------------------------------------")
    

    str1 = checker.forest1.__str__()
    str2 = checker.forest2.__str__()
    
    
    start_time = time.time()
    numIter:int = 1000000
    for i in range(numIter):
        distance = Levenshtein.distance(str1, str2)
    end_time = time.time()
    
    print("distance ",distance)
    print("Iter: ", numIter,"time: ", end_time-start_time)
    

if __name__ == "__main__":
    main()
