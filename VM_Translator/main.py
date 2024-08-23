class Main:
    def __init__(self,codewriter,parser,vm_filename):
        codewriter(vm_filename,parser)

if __name__ == '__main__':
    import sys 
    from codewriter import CodeWriter
    from my_parser import Parser

    vm_filename = sys.argv[1]
    Main(CodeWriter,Parser,vm_filename)