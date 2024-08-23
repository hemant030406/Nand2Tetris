
import re,os

class CompilationEngine:

    def __init__(self,inputFile,outputFile):
        from SymbolTable import SymbolTable
        from VMWriter import VMWriter
        self.symtab = SymbolTable()
        self.vmw = VMWriter(outputFile)
        self.inputFile = open(inputFile,'r')
        self.currInst = ''
        self.className = ''
        self.whileNum = 0
        self.IFNum = 0
        self.compileClass()
        self.inputFile.close()
        self.vmw.close()
        os.remove(inputFile)

    def getNextLine(self):
        self.currInst = self.inputFile.readline().strip()
        while not self.currInst:
            self.currInst = self.inputFile.readline().strip()

    def getres(self,str):
        return re.findall(f'<{str}>(.*?)</{str}>',self.currInst)[0]

    def compileClass(self):

        #'<tokens>'
        self.getNextLine()
        #'class'
        self.getNextLine()

        #'class'
        self.getNextLine()

        #'className'
        self.className = self.getres('identifier')
        self.getNextLine()

        #'{'
        self.getNextLine()

        #classVarDec
        if 'field' in self.currInst or 'static' in self.currInst:
            while 'field' in self.currInst or 'static' in self.currInst:
                self.compileClassVarDec()

        #subRoutine
        while 'constructor' in self.currInst or 'function' in self.currInst or 'method' in self.currInst:
            self.symtab.reset()
            self.compileSubRoutine()
        

    def compileLet(self):

        #'let'
        self.getNextLine()

        #'varName'
        varName = self.getres('identifier')
        seg = self.symtab.kindOf(varName)
        index = self.symtab.indexOf(varName)
        self.getNextLine()

        #'[expression]'?
        if '[' in self.currInst:
            self.vmw.writePush(seg,index)

            #'['
            self.getNextLine()

            #expression
            self.compileExpression()
            self.vmw.writeArithmetic('add')

            #']'
            self.getNextLine()

            #'='
            self.getNextLine()

            self.compileExpression()
            self.vmw.writePop('temp',0)
            self.vmw.writePop('pointer',1)
            self.vmw.writePush('temp',0)
            self.vmw.writePop('that',0)
        
        else:
            #'='
            self.getNextLine()

            self.compileExpression()
            self.vmw.writePop(seg,index)

        #';'
        self.getNextLine()


    def compileIf(self):
        ifENDLabel = f'IF_END{self.IFNum}'
        elseLabel = f'ELSE{self.IFNum}'
        self.IFNum += 1
        
        #'if'
        self.getNextLine()

        #'('
        self.getNextLine()

        #'expression'
        self.compileExpression()
        self.vmw.writeArithmetic('not')
        self.vmw.writeIf(elseLabel)
        
        #')'
        self.getNextLine()

        #'{'
        self.getNextLine()

        #'statements'
        self.compileStatements()
        self.vmw.writeGoto(ifENDLabel)
        self.vmw.writeLabel(elseLabel)

        #'}'
        self.getNextLine()

        #'elseStatement'
        if 'else' in self.currInst:
            #'else'
            self.getNextLine()

            #'{'
            self.getNextLine()

            #'statements'
            self.compileStatements()

            #'}'
            self.getNextLine()
        self.vmw.writeLabel(ifENDLabel)


    def compileWhile(self):
        whileStart = f'WHILE_START{self.whileNum}'
        whileEND = f'WHILE_END{self.whileNum}'
        self.whileNum += 1
        #'while'
        self.getNextLine()

        #'('
        self.getNextLine()

        #'expression'
        self.vmw.writeLabel(whileStart)
        self.compileExpression()
        self.vmw.writeArithmetic('not')
        self.vmw.writeIf(whileEND)

        #')'
        self.getNextLine()

        #'{'
        self.getNextLine()

        #'statements'
        self.compileStatements()
        self.vmw.writeGoto(whileStart)
        self.vmw.writeLabel(whileEND)

        #'}'
        self.getNextLine()


    def compileDo(self):
        #'do'
        self.getNextLine()

        #subroutineName
        subName = self.getres('identifier')
        self.getNextLine()

        #'subroutineCall'
        self.compileSubRoutineCall(subName)
        self.vmw.writePop('temp',0)

        #';'
        self.getNextLine()


    def compileReturn(self):

        #'return'
        self.getNextLine()

        #'expression'
        if ';' not in self.currInst:
            self.compileExpression()
        else:
            self.vmw.writePush('constant',0)

        self.vmw.writeReturn()

        #';'
        self.getNextLine()
        

    def compileTerm(self):
        #'(expression)'
        if '(' in self.currInst:
            #'('
            self.getNextLine()
            #'expression'
            self.compileExpression()
            #')'
            self.getNextLine()

        #'varName','subroutineCall','varName[expression]'
        elif '<identifier>' in self.currInst:
            #'varName'
            varName = self.getres('identifier')
            seg = self.symtab.kindOf(varName)
            idx = self.symtab.indexOf(varName)
            self.getNextLine()
            #'[expression]'
            if '[' in self.currInst:
                self.vmw.writePush(seg,idx)
                #'['
                self.getNextLine()
                #'expression'
                self.compileExpression()
                self.vmw.writeArithmetic('add')
                self.vmw.writePop('pointer',1)
                self.vmw.writePush('that',0)
                #']'
                self.getNextLine()
            #'subroutineCall'
            elif '(' in self.currInst or '.' in self.currInst:  
                self.compileSubRoutineCall(varName)
            else:
                self.vmw.writePush(seg,idx)

        #'unaryOp term'
        elif '-' in self.currInst or '~' in self.currInst:
            uOp = self.getres('symbol')
            self.getNextLine()
            self.compileTerm()
            if uOp == '-':
                self.vmw.writeArithmetic('neg')
            elif uOp == '~':
                self.vmw.writeArithmetic('not')

        #integerConst
        elif '<integerConstant>' in self.currInst:
            self.vmw.writePush('constant',self.getres("integerConstant"))
            self.getNextLine()

        #stringConst
        elif '<stringConstant>' in self.currInst:
            str = self.getres('stringConstant')
            self.vmw.writePush('constant',len(str))
            self.vmw.writeCall('String.new',1)
            for i in str:
                self.vmw.writePush('constant',ord(i))
                self.vmw.writeCall('String.appendChar',2)
            self.getNextLine()

        # keywordconst = ['true','false','null','this']
        elif '<keyword>' in self.currInst:
            if self.getres('keyword') == 'true':
                self.vmw.writePush('constant','1')
                self.vmw.writeArithmetic('neg')

            elif self.getres('keyword') == 'false':
                self.vmw.writePush('constant','0')

            elif self.getres('keyword') == 'null':
                self.vmw.writePush('constant','0')

            elif self.getres('keyword') == 'this':
                self.vmw.writePush('pointer','0')

            self.getNextLine()

        else:
            self.getNextLine()
        

    def compileExpression(self):
        #'term'
        self.compileTerm()

        #'(op term)*'
        while any(['+' in self.currInst,'-' in self.currInst,'*' in self.currInst,'<symbol>/' in self.currInst,'&amp;' in self.currInst,'|' in self.currInst,'&lt;' in self.currInst,'&gt;' in self.currInst,'=' in self.currInst]):
            oper = self.getres('symbol')
            self.getNextLine()
            if oper == '+':
                self.compileTerm()
                self.vmw.writeArithmetic('add')
            elif oper == '-':
                self.compileTerm()
                self.vmw.writeArithmetic('sub')
            elif oper == '*':
                self.compileTerm()
                self.vmw.writeCall('Math.multiply',2)
            elif oper == '/':
                self.compileTerm()
                self.vmw.writeCall('Math.divide',2)
            elif oper == '&amp;':
                self.compileTerm()
                self.vmw.writeArithmetic('and')
            elif oper == '|':
                self.compileTerm()
                self.vmw.writeArithmetic('or')
            elif oper == '&lt;':
                self.compileTerm()
                self.vmw.writeArithmetic('lt')
            elif oper == '&gt;':
                self.compileTerm()
                self.vmw.writeArithmetic('gt')
            elif oper == '=':
                self.compileTerm()
                self.vmw.writeArithmetic('eq')
            
    
    def compileSubRoutineCall(self,subName):
        if '(' in self.currInst:
            #'('
            self.getNextLine()
            #'expressionList'
            self.nArgs = 0
            self.vmw.writePush('pointer',0)
            self.nArgs += 1 
            self.compileExpressionList()
            self.vmw.writeCall(f'{self.className}.{subName}',self.nArgs)
            #')'
            self.getNextLine()

        elif '.' in self.currInst:
            #'.'
            self.getNextLine()
            #'subroutinName'
            self.subName1 = self.getres('identifier')
            self.getNextLine()
            #'('
            self.getNextLine()

            #'expressionList'
            self.nArgs = 0
            if self.symtab.typeOf(subName) != None:
                if self.symtab.typeOf(subName)[0].isupper():
                    self.nArgs += 1
                    self.vmw.writePush(self.symtab.kindOf(subName),self.symtab.indexOf(subName))
                    self.compileExpressionList()
                    self.vmw.writeCall(f'{self.symtab.typeOf(subName)}.{self.subName1}',self.nArgs)
            else:
                self.compileExpressionList()
                self.vmw.writeCall(f'{subName}.{self.subName1}',self.nArgs)

            #')'
            self.getNextLine()

            
    def compileExpressionList(self):
        while ')' not in self.currInst:
            if ',' in self.currInst:
                #','
                self.getNextLine()
            else:
                self.nArgs += 1
                self.compileExpression()


    def compileClassVarDec(self):

        #'field,static'
        kind = self.getres('keyword')
        self.getNextLine()

        #'int,char,boolean'
        if 'keyword' in self.currInst:
            type = self.getres('keyword')
        #'className'
        elif 'identifier' in self.currInst:
            type = self.getres('identifier')

        self.getNextLine()

        while ';' not in self.currInst:
            #varName
            if ',' not in self.currInst:
                name = self.getres('identifier')
                self.symtab.define(name,type,kind)

            self.getNextLine()

        #';'
        self.getNextLine()


    def compileSubRoutine(self):

        #'constructor' or 'function' or 'method'
        self.subroutineType = self.getres('keyword')
        self.getNextLine()

        #'void|type'
        self.getNextLine()

        #'subroutineName'
        self.subroutineName = self.getres('identifier')
        self.getNextLine()

        #'('
        self.getNextLine()

        #'parameterList'
        if self.subroutineType == 'method':
            self.symtab.define('this',self.className,'argument')
        self.compileParameterList()

        #')'
        self.getNextLine()

        self.compileSubRoutineBody()

                    
    def compileSubRoutineBody(self):

        #'{'
        self.getNextLine()

        while 'var' in self.currInst:
            self.compileVarDec()
        
        nVars = self.symtab.varCount('local')
        self.vmw.writeFunction(f'{self.className}.{self.subroutineName}',nVars)
        
        if self.subroutineType == 'constructor':
            nFields = self.symtab.varCount('this')
            self.vmw.writePush('constant',nFields)
            self.vmw.writeCall('Memory.alloc',1)
            self.vmw.writePop('pointer',0)

        elif self.subroutineType == 'method':
            self.vmw.writePush('argument',0)
            self.vmw.writePop('pointer',0)

        self.compileStatements()

        #'}'
        self.getNextLine()


    def compileVarDec(self):
        #'var'
        kind = 'local'
        self.getNextLine()

        #'int,char,boolean'
        if 'keyword' in self.currInst:
            type = self.getres('keyword')
        #'className'
        elif 'identifier' in self.currInst:
            type = self.getres('identifier')

        self.getNextLine()

        while ';' not in self.currInst:
            #varName
            if ',' not in self.currInst:
                name = self.getres('identifier')
                self.symtab.define(name,type,kind)
            self.getNextLine()

        #';'
        self.getNextLine()


    def compileParameterList(self):
        count = 1
        kind = 'argument'
        while ')' not in self.currInst:
            if count%3 == 1:
                if 'keyword' in self.currInst:
                    type = self.getres('keyword')
                elif 'identifier' in self.currInst:
                    type = self.getres('identifier')
            elif count%3 == 2:
                name = self.getres('identifier')
                self.symtab.define(name,type,kind)
            count +=1 
            self.getNextLine()


    def compileStatements(self):
        if '}' not in self.currInst:
            while '}' not in self.currInst:
                if 'let' in self.currInst:
                    self.compileLet()
                elif 'if' in self.currInst:
                    self.compileIf()
                elif 'while' in self.currInst:
                    self.compileWhile()
                elif 'do' in self.currInst:
                    self.compileDo()
                elif 'return' in self.currInst:
                    self.compileReturn()
