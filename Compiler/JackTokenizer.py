class JackTokenizer:
    def __init__(self,inputFile):
        if '\\' in inputFile:
            self.outputFilename = '\\'.join(inputFile.split('\\')[0:-1]) +'\\' + inputFile.split('\\')[-1].replace('.jack','T.xml')
        elif '/' in inputFile:
            self.outputFilename = '/'.join(inputFile.split('/')[0:-1]) +'/' + inputFile.split('/')[-1].replace('.jack','T.xml')
        self.file = open(inputFile,'r')
        self.totalLines = len(self.file.readlines())

        self.file.close()

        self.file = open(inputFile,'r')
        self.currInst = self.file.readline().strip()

        self.instNum = 0
        self.charNum = -1
        self.currChar = ''
        self.tokenList = []
        self.currToken = ''

        self.keyword = {'class':0 , 'constructor':1 , 'function':2 ,
                        'method':3 , 'field':4 , 'static':5 , 'var':6 , 'int':7 ,
                        'char':8 , 'boolean':9 , 'void':10 , 'true':11 , 'false':12 ,
                        'null':13 , 'this':14 , 'let':15 , 'do':16 , 'if':17 , 'else':18 ,
                        'while':19 , 'return':20}
        
        self.symbol = {'{':0 , '}':1 , '(':2 , ')':3 , '[':4 , ']':5 , '.':6 , ',':7 , ';':8 , '+':9 , '-':10 , '*':11 ,'/':12 , '&':13 , '|':14 , '<':15 , '>':16 , '=':17 , '~':18}
        

        self.advance()
        self.remove_comment()
        while self.hasMoreLines():
            self.createTokens()
            
        self.createXml()


    def hasMoreLines(self):
        return self.instNum < self.totalLines 
    
    def hasMoreTokens(self):
        return self.charNum < len(self.currInst) - 1
    
    def advance(self):

        if self.hasMoreTokens():
            self.charNum += 1
            self.currChar = self.currInst[self.charNum]
            
        else:
            self.charNum = 0
            self.currInst = self.file.readline().strip()
            self.instNum += 1

            while self.hasMoreLines() and not self.currInst:
                self.currInst = self.file.readline().strip()
                self.instNum += 1

            if self.currInst:
                self.currChar = self.currInst[0]

            
    def remove_comment(self):

        while self.currChar == '/' and self.hasMoreTokens() and self.currInst[:self.currInst.index(self.currChar)].count('"')%2==0:
                
                if self.currInst[self.charNum + 1]=='/':

                    self.currInst = self.file.readline().strip()
                    self.instNum += 1

                    while self.hasMoreLines() and not self.currInst:
                        self.currInst = self.file.readline().strip()
                        self.instNum += 1
                    
                    if self.currInst:
                        self.currChar = self.currInst[0]
                        self.charNum = 0

                elif self.currInst[self.charNum + 1]=='*':

                    self.advance()

                    if self.hasMoreTokens():
                        while not(self.currChar == '*' and self.currInst[self.charNum + 1]=='/'):
                            self.advance()
                            while not self.hasMoreTokens():
                                self.advance()
                        self.advance()
                        self.advance()

                    else:

                        self.advance()

                        while not(self.currChar == '*' and self.currInst[self.charNum + 1]=='/'):
                            self.advance()
                            while not self.hasMoreTokens():
                                self.advance()
                        self.advance()
                        self.advance()

                else:
                    return 


    def createTokens(self):
        
        if self.currChar in self.symbol:
            self.currToken = self.currChar
            self.tokenList.append(self.currToken)
            self.currToken = ''
            self.advance()
            self.remove_comment()
            

        elif self.currChar == '"':
            self.currToken += self.currChar
            self.charNum += 1
            self.currChar = self.currInst[self.charNum]

            while self.currChar != '"':
                self.currToken += self.currChar
                self.advance()
                self.remove_comment()
                
            self.advance()
            self.remove_comment()
            
            self.currToken+='"'
            self.tokenList.append(self.currToken)
            self.currToken = ''

        elif self.currChar.isalpha():

            while self.currChar != ' ' and self.currChar not in self.symbol and self.currChar != '"':
                self.currToken += self.currChar
                self.advance()
                self.remove_comment()
                
            self.tokenList.append(self.currToken)
            self.currToken = ''
        
        elif self.currChar.isdigit():

            while self.currChar != ' ' and self.currChar not in self.symbol and self.currChar != '"':
                self.currToken += self.currChar
                self.advance()
                self.remove_comment()
                
            self.tokenList.append(self.currToken)
            self.currToken = ''

        elif self.currChar == ' ':
            self.advance()
            self.remove_comment()

        else:
            self.remove_comment()
            

    def createXml(self):

        outputfile = open(self.outputFilename,'w')
        outputfile.write('<tokens>\n')

        for i in self.tokenList:

            if i in self.keyword:
                outputfile.write(f'<keyword>{i}</keyword>\n')

            elif i in self.symbol:
                if i == '<':
                    i = '&lt;'

                elif i == '>':
                    i = '&gt;'

                elif i == '"':
                    i = '&quot;'

                elif i == '&':
                    i = '&amp;'

                outputfile.write(f'<symbol>{i}</symbol>\n')

            elif i[0]=='"':
                outputfile.write(f'<stringConstant>{i[1:-1]}</stringConstant>\n')

            elif i.isdigit():
                outputfile.write(f'<integerConstant>{i}</integerConstant>\n')

            else:
                outputfile.write(f'<identifier>{i}</identifier>\n')

        outputfile.write('</tokens>')
        outputfile.close()


