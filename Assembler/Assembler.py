import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

class Assembler:
    def __init__(self, parser, symbol_table, code):
        self.parser = parser
        self.symbol_table = symbol_table
        self.code = code

    def assemble(self, asm_filename):
        self.prepare_files(asm_filename)
        parser = self.parser

        # First pass to build label table
        while parser.hasMoreLines():
            parser.advance()
            if parser.instruction_type == 'L_INSTRUCTION':
                self.write_L(parser.symbol)

        # Second pass to write .hack file
        parser.reset_file()
        self.ram_address = 16
        while parser.hasMoreLines():
            parser.advance()
            if parser.instruction_type == 'A_INSTRUCTION':
                self.write_A(parser.symbol)
            elif parser.instruction_type == 'C_INSTRUCTION':
                self.write_C(parser.dest, parser.comp, parser.jump)

        parser.close_file()
        self.hack.close()

    def prepare_files(self, asm_filename):
        assert '.asm' in asm_filename, 'Must pass .asm file!'
        self.parser.load_file(asm_filename)
        hack_filename = asm_filename.replace('.asm', '.hack')
        self.hack = open(hack_filename, 'w')

    def create_address(self, symbol):
        address = '{0:b}'.format(int(symbol))
        base = (15 - len(address)) * '0'
        return base + address

    def write(self, instruction):
        self.hack.write(instruction + '\n')

    def write_A(self, symbol):
        instruction = '0'
        try:
            int(symbol)
        except ValueError:
            # Build table on first pass
            if not self.symbol_table.contains(symbol):
                address = self.create_address(self.ram_address)
                self.symbol_table.addEntry(symbol, address)
                self.ram_address += 1
            instruction += self.symbol_table.getAddress(symbol)
        else:
            instruction += self.create_address(symbol)

        self.write(instruction)

    def write_L(self, symbol):
        address = self.create_address(self.parser.instr_num+1)
        self.symbol_table.addEntry(symbol, address)

    def write_C(self, dest, comp, jump):
        instruction = '111'
        instruction += self.code.comp(comp)
        instruction += self.code.dest(dest)
        instruction += self.code.jump(jump)
        self.write(instruction)

if __name__ == '__main__':
    asm_filename = sys.argv[1]
    assembler = Assembler(Parser(), SymbolTable(), Code())
    assembler.assemble(asm_filename)