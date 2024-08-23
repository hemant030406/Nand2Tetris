class JackCompiler:
    pass 

if __name__ == '__main__':
    import sys,os;
    from JackTokenizer import JackTokenizer
    from CompilationEngine import CompilationEngine

    inputFile = sys.argv[1]

    if inputFile.endswith('.jack'):
        JackTokenizer(inputFile)
        CompilationEngine(inputFile.replace('.jack','T.xml'),inputFile.replace('.jack','.vm'))

    else:
        for filename in os.listdir(inputFile):
            if filename.endswith('.jack'):
                JackTokenizer(os.path.join(inputFile,filename))
                CompilationEngine(os.path.join(inputFile,filename.replace('.jack','T.xml')),os.path.join(inputFile,filename.replace('.jack','.vm')))