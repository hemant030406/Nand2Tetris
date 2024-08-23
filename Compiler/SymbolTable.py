class SymbolTable:

    def __init__(self):
        self.classTable = []
        self.subroutineTable = []
        self.SIndex = 0
        self.FIndex = 0
        self.AIndex = 0
        self.VIndex = 0

    def reset(self):
        self.subroutineTable = []
        self.AIndex = 0
        self.VIndex = 0

    def define(self,name,type,kind):
        if kind == 'static' or kind == 'field':
            if kind == 'static':
                self.classTable.append({'name':name,'type':type,'kind':kind,'index':self.SIndex})
                self.SIndex += 1
            elif kind == 'field':
                self.classTable.append({'name':name,'type':type,'kind':"this",'index':self.FIndex})
                self.FIndex += 1
        else:
            if kind == 'argument':
                self.subroutineTable.append({'name':name,'type':type,'kind':kind,'index':self.AIndex})
                self.AIndex += 1
            if kind == 'local':
                self.subroutineTable.append({'name':name,'type':type,'kind':kind,'index':self.VIndex})
                self.VIndex += 1

    def varCount(self,kind):
        count = 0
        if kind == 'static' or kind == 'this':
            for i in range(len(self.classTable)):
                if self.classTable[i]['kind'] == kind:
                    count +=1 
            return count 
        else:
            for i in range(len(self.subroutineTable)):
                if self.subroutineTable[i]['kind'] == kind:
                    count +=1 
            return count 

    def kindOf(self,name):
        for i in range(len(self.classTable)):
            if self.classTable[i]['name'] == name:
                return self.classTable[i]['kind']
        for i in range(len(self.subroutineTable)):
            if self.subroutineTable[i]['name'] == name:
                return self.subroutineTable[i]['kind']
        return 'NONE'

    def typeOf(self,name):
        for i in range(len(self.classTable)):
            if self.classTable[i]['name'] == name:
                return self.classTable[i]['type']
        for i in range(len(self.subroutineTable)):
            if self.subroutineTable[i]['name'] == name:
                return self.subroutineTable[i]['type']

    def indexOf(self,name):
        for i in range(len(self.classTable)):
            if self.classTable[i]['name'] == name:
                return self.classTable[i]['index']
        for i in range(len(self.subroutineTable)):
            if self.subroutineTable[i]['name'] == name:
                return self.subroutineTable[i]['index']