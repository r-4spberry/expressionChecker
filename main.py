import my_parser
import lark

def main():
    parser :my_parser.my_parser 
    parser = my_parser.my_parser()
    
    
    res : lark.Tree = parser.parse("integral(2 + 5,2,2) +19 + 98 * 92 +64* sum(2,var(a))")
    print(res.pretty())
    
    
    
if __name__ == "__main__":
    main()

