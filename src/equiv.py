import lark
from lark import Tree, Token
from normalize import NormalizeTree
from typing import List


class Equiv:
    "This class is used to produce equivalents of different lark.Trees with our grammar"

    @staticmethod
    def getEquiv(equation: lark.Tree) -> List[lark.Tree]:
        "Function to get equivalents"

        ret: List = []

        if not isinstance(equation, Tree):
            return ret

        ret = ret + Equiv.ruleExpandBrackets(equation)
        ret = ret + Equiv.ruleCombineSum(equation)
        ret = ret + Equiv.ruleCombineMul(equation)
        ret = ret + Equiv.ruleInvertFraq(equation)
        ret = ret + Equiv.ruleMutiplyAllNumbers(equation)
        ret = ret + Equiv.ruleCombinePowers(equation)

        return ret

    @staticmethod
    def ruleExpandBrackets(equation: Tree) -> List[Tree]:
        "((a+b+c)*d) = (a*d + b*d + c*d)"
        ret: List = []
        if equation.data == "mul":

            ch: List = []
            ch = equation.children

            # Is there a sum in mul? can we expand brackets?
            sumElem: Tree = None
            others: List[Tree] = []

            for elem in ch:
                if sumElem is None:
                    if elem.data == "sum":
                        sumElem = elem
                    else:
                        others.append(elem)
                else:
                    others.append(elem)

            # There is a sum in mul - expanding brackets
            if sumElem is not None:

                resElem: Tree
                resChildren: list[Tree] = []
                for nom in sumElem.children:
                    resChildren.append(Tree("mul", others + [nom]))
                resElem = Tree("sum", resChildren)
                ret.append(resElem)
                # print(resElem.pretty())
                # print("----debug mul ----")

        return ret

    @staticmethod
    def ruleCombineSum(equation: Tree) -> List[Tree]:
        "((a + b) + (c + d)) = (a + b + c + d)"
        ret: List[Tree] = []
        if equation.data == "sum":
            arr: List[Tree] = []
            for ch in equation.children:
                if ch.data == "sum":
                    arr = arr + ch.children
                else:
                    arr.append(ch)
            if len(arr) > len(equation.children):
                resElem: Tree = Tree("sum", arr)
                ret.append(resElem)
            elif len(arr) == 1:
                ret.append(arr[0])

        return ret

    @staticmethod
    def ruleCombineMul(equation: Tree) -> List[Tree]:
        "((a * b) * (c * d)) = (a * b * c * d)"
        ret: List[Tree] = []
        if equation.data == "mul":
            arr: List[Tree] = []
            for ch in equation.children:
                if ch.data == "mul":
                    arr = arr + ch.children
                else:
                    arr.append(ch)
            if len(arr) > len(equation.children):
                resElem: Tree = Tree("mul", arr)
                ret.append(resElem)
            elif len(arr) == 1:
                ret.append(arr[0])

        return ret

    @staticmethod
    def ruleInvertFraq(equation: Tree) -> List[Tree]:
        "(a / b) = (a * (b ** -1))"
        ret: List[Tree] = []
        if equation.data == "fraq" and len(equation.children) == 2:
            arr: List[Tree] = []
            arr = arr + [equation.children[0]]

            powArr: List[Tree] = []
            powArr = powArr + [equation.children[1]]
            powArr = powArr + [Tree("num", [Token("NUMBER", "-1")])]

            arr = arr + [Tree("pow", powArr)]

            resElem: Tree = Tree("mul", arr)

            ret = ret + [resElem]

        return ret

    @staticmethod
    def ruleMutiplyAllNumbers(equation: Tree) -> List[Tree]:
        "(a * 100 * -8 * k) = (-800 * a * k)"
        ret: List[Tree] = []
        if equation.data == "mul":
            arr = []
            nom: int = 1
            numMultipliers: int = 0
            for ch in equation.children:
                if ch.data == "num":
                    val: float = float(ch.children[0].value)
                    nom = nom * val
                    numMultipliers +=1
                else:
                    arr = arr + [ch]

            if numMultipliers > 1:
            
                if nom != 1:
                    arr.append(Tree("num", [Token("NUMBER", str(nom))]))
                elif nom == 1 and len(arr) == 0:
                    arr.append(Tree("num", [Token("NUMBER", str(nom))]))

                
                if len(arr) == 1:
                    resElem: Tree = arr[0]
                    ret = ret + [resElem]
                elif len(arr) > 1:
                    resElem: Tree = Tree("mul", arr)
                    ret = ret + [resElem]

        return ret

    @staticmethod
    def ruleCombinePowers(equation: Tree) -> List[Tree]:
        "((a**b) * (a**c) * 888 * (a**67)) = ((a**(b + c + 67)) * 888)"
        ret: List[Tree] = []
        if equation.data == "mul":
            powArr: List[Tree] = []
            nonPowArr: List[Tree] = []

            # divide factors into powers / non-powers
            for ch in equation.children:
                if ch.data == "pow":
                    powArr = powArr + [ch]
                else:
                    nonPowArr = nonPowArr + [ch]

            base: Tree = None

            if len(powArr) > 1:

                # try to find powers with the same base
                for i in range(len(powArr)):
                    if base is not None:
                        break
                    for j in range(i + 1, len(powArr), 1):
                        if base is not None:
                            break
                        if powArr[i].children[0] == powArr[j].children[0]:
                            base = powArr[i].children[0]

                # found powers with the same base - create a new equivalent
                if base is not None:
                    sumArr: List[Tree] = []
                    otherPowArr: List[Tree] = []
                    for ch in powArr:
                        if base == ch.children[0]:
                            sumArr = sumArr + [ch.children[1]]
                        else:
                            otherPowArr = otherPowArr + [ch]
                            
                    if len(sumArr) > 1:
                        powElem: Tree = Tree("pow", [base, Tree("sum", sumArr)])

                        resArr: List[Tree] = nonPowArr + [powElem] + otherPowArr

                        if len(resArr) == 1:
                            retElem = resArr[0]
                            ret = ret + [retElem]
                        elif len(resArr) > 1:
                            retElem = Tree("mul", resArr)
                            ret = ret + [retElem]

        return ret
