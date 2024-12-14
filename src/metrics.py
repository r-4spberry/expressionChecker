from rapidfuzz.distance import Levenshtein


class Metrics:
    @staticmethod
    def levenshteinMetric(r1:str,e1:str,e2:str,r2:str) -> int:
        "computes metric as the sum of Levenstein distances in the following path: root1->eq1->eq2->root2"
        return Levenshtein.distance(r1,e1) + Levenshtein.distance(e1,e2) + Levenshtein.distance(e2,r1)