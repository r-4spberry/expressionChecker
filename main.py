import my_parser
import lark
from equiv import Equiv
from searchnode import SearchNode


def main():
    parser: my_parser.MyParser
    parser = my_parser.MyParser()

    # res: lark.Tree = parser.parse(
    #     "sum( \
    #         var(a),\
    #         var(e),\
    #         var(c),\
    #         var(c),\
    #         num(888),\
    #         sum(\
    #             var(g),\
    #             num(77),\
    #             fraq(\
    #                 num(888),\
    #                 num(999)\
    #             )\
    #         )\
    #     )"
    # )
    # print(res.pretty())

    # normalizer: my_parser.NormalizeTree = my_parser.NormalizeTree()
    # norm_res: lark.Tree = normalizer.transform(res)
    # print(norm_res.pretty())
    # print(norm_res)
    
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
    
    node = SearchNode(equation)
    
    print(node.tree.pretty())
    node.findChildNodes()
    print("equivalents: ")
    for i in node.childNodes:
        print("------------------------------------------------------------")
        print(i.tree.pretty())



if __name__ == "__main__":
    main()
