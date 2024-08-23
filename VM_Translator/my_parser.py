class Parser:
    def __init__(self,vm_filename):
        f = open(vm_filename,'r')
        lines = f.readlines()
        self.lines = []
        for i in lines:
            i=i.split('\n')[0]
            i=i.split('//')[0]
            i=i.strip()
            if i:
                self.lines.append(i)
    
        self.total_lines = len(self.lines) - 1
        self.instr_num = -1
        self.curr_instr = None

    def hasMoreLines(self):
        return self.instr_num < self.total_lines 
    
    def advance(self):
        if self.hasMoreLines():
            self.instr_num += 1
            self.curr_instr = self.lines[self.instr_num]

    def commandType(self):
        if self.curr_instr.startswith('push'):
            return 'push_command'
        elif self.curr_instr.startswith('pop'):
            return 'pop_command'
        else:
            return 'arithmetic_command'
        
    def arg1(self):
        li = self.curr_instr.split()
        if len(li)>=2:
            return li[1]
        
    def arg2(self):
        li = self.curr_instr.split()
        if len(li)>=3:
            return li[2]
