import my_parser
import lark
from equiv import Equiv


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
    
    res: lark.Tree = parser.parse(
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
                )\
            )\
        )"
    )
    print(res.pretty())
    eq = Equiv.getEquiv(res.children[0])
    print(eq[0].pretty())


if __name__ == "__main__":
    main()
