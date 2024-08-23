import os
class CodeWriter:
    def __init__(self, vm_filename, parser):
        self.parser = parser(vm_filename)
        asm_filename = vm_filename.replace('.vm', '.asm')
        self.asm_file = open(asm_filename, 'w')
        self.static_var = os.path.basename(vm_filename).replace('.vm', '.')
        self.label_var = 0

        while self.parser.hasMoreLines():
            self.parser.advance()
            self.command = self.parser.commandType()
            if self.command == 'push_command' or self.command == 'pop_command':
                self.writePushPop()
                self.asm_file.write(self.string)
            else:
                self.writeArithmetic()
                self.asm_file.write(self.string)

        self.close()

    def gen_push_str(self,segment,index):
        
        pref = {
            'local': '@LCL',
            'argument': '@ARG',
            'this': '@THIS',
            'that': '@THAT',
            'temp': f'@{5+int(index)}',
            'pointer': f'@{"THIS" if index=="0" else "THAT"}',
            'constant': f'@{index}',
            'static': f'@{self.static_var+index}'
        }

        mid = f'\nD=M\n@{index}\nA=D+A'
        suf = f'\nD={'A' if segment[:4] == 'cons' else 'M'}\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        suf_d = {
            'local': mid + suf,
            'argument': mid + suf,
            'this': mid + suf,
            'that': mid + suf,
            'temp': suf,
            'pointer': suf,
            'constant': suf,
            'static': suf
        }

        return pref[segment] + suf_d[segment]
    
    def gen_pop_str(self,segment,index):
        
        pref = {
            'local': '@LCL',
            'argument': '@ARG',
            'this': '@THIS',
            'that': '@THAT'
        }

        mid = {
            'temp': f'{5+int(index)}',
            'pointer': f'{"THIS" if index == "0" else "THAT"}',
            'static': f'{self.static_var+index}'
        }

        suf_latt = f'\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
        rem = f'@SP\nM=M-1\nA=M\nD=M\n@{mid[segment]}\nM=D\n'

        d = {
            'local': pref[segment] + suf_latt,
            'argument': pref[segment] + suf_latt,
            'this': pref[segment] + suf_latt,
            'that': pref[segment] + suf_latt,
            'temp': rem,
            'pointer': rem,
            'static': rem
        }

        return d[segment]

    def writePushPop(self):
        segment = self.parser.arg1()
        index = self.parser.arg2()

        if self.command == 'push_command':
            self.string = self.gen_push_str(segment,index)

        elif self.command == 'pop_command':
            self.string = self.gen_pop_str(segment,index)

    def writeArithmetic(self):
        inst = self.parser.curr_instr.split()[0]
        match inst:
            case 'add':
                self.string = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M\n'
            
            case 'sub':
                self.string = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n'
            
            case 'neg':
                self.string = '@SP\nA=M-1\nM=-M\n'
            
            case 'not':
                self.string = '@SP\nA=M-1\nM=!M\n'
            
            case 'eq':
                self.string = f'@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\nM=-1\n@EQUAL{str(self.label_var)}\nD;JEQ\n@SP\nA=M-1\nM=0\n(EQUAL{str(self.label_var)})\n'
                self.label_var += 1
            
            case 'gt':
                self.string = f'@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\nM=-1\n@GT{str(self.label_var)}\nD;JGT\n@SP\nA=M-1\nM=0\n(GT{str(self.label_var)})\n'
                self.label_var += 1
            
            case 'lt':
                self.string = f'@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\nM=-1\n@LT{str(self.label_var)}\nD;JLT\n@SP\nA=M-1\nM=0\n(LT{str(self.label_var)})\n'
                self.label_var += 1
            
            case 'and':
                self.string = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M&D\n'
            
            case 'or':
                self.string = '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M|D\n'

    def close(self):
        self.asm_file.close()
