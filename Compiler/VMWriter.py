class VMWriter:
    def __init__(self,outputFile):
        self.file = open(outputFile,'w') 

    def writePush(self,segment,index):
        self.file.write(f'push {segment} {index}\n')

    def writePop(self,segment,index):
        self.file.write(f'pop {segment} {index}\n')

    def writeArithmetic(self,command):
        self.file.write(f'{command}\n')

    def writeLabel(self,label):
        self.file.write(f'label {label}\n')

    def writeGoto(self,label):
        self.file.write(f'goto {label}\n')

    def writeIf(self,label):
        self.file.write(f'if-goto {label}\n')

    def writeCall(self,name,nArgs):
        self.file.write(f'call {name} {nArgs}\n')

    def writeFunction(self,name,nVars):
        self.file.write(f'function {name} {nVars}\n')

    def writeReturn(self):
        self.file.write('return\n') 

    def close(self):
        self.file.close()

    
