class Parser:
    
    def load_file(self, asm_filename):
        self.file = open(asm_filename, 'r')
        self.reset_file()
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.instruction_type = None

    def reset_file(self):
        self.file.seek(0)
        line = self.file.readline().strip()
        while self.is_not_instruction(line):
            line = self.file.readline().strip()
        self.current_instruction = line
        self.instr_num = -1

    def close_file(self):
        self.file.close()

    def is_not_instruction(self, line):
        return not line or line[:2] == '//'

    def hasMoreLines(self):
        return bool(self.current_instruction)

    def get_next_instruction(self):
        line = self.file.readline().strip()
        line = line.split('//')[0]
        line = line.strip()
        self.current_instruction = line

    def advance(self):
        ci = self.current_instruction
        self.instructionType(ci)
        if ci[0] == '@':
            self.instr_num += 1
        elif ci[0] == '(':
            pass
        else:
            self.instr_num += 1
        self.get_next_instruction()

    def instructionType(self, line):
        if line[0] == '@':
            self.symbol = line[1:]
            self.instruction_type = 'A_INSTRUCTION'
        elif line[0] == '(':
            self.symbol = line[1:-1]
            self.instruction_type = 'L_INSTRUCTION'
        else:
            self.dest, self.comp, self.jump = None, None, None
            parts = line.split(';')
            remainder = parts[0]
            if len(parts) == 2:
                self.jump = parts[1]
            parts = remainder.split('=')
            if len(parts) == 2:
                self.dest = parts[0]
                self.comp = parts[1]
            else:
                self.comp = parts[0]
            self.instruction_type = 'C_INSTRUCTION'
