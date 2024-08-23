class Code:
    def dest(self, destination):
        dest_list = ['0', '0', '0']
        if not destination:
            return ''.join(dest_list)
        if 'A' in destination:
            dest_list[0] = '1'
        if 'D' in destination:
            dest_list[1] = '1'
        if 'M' in destination:
            dest_list[2] = '1'
        return ''.join(dest_list)

    def comp(self, computation):
        comp_dict = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101'
        }
        a_bit = '0'
        if 'M' in computation:
            a_bit = '1'
            computation = computation.replace('M', 'A')
        c_bit = comp_dict.get(computation, '000000')
        return a_bit + c_bit

    def jump(self, jump_name):
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jump_dict.get(jump_name, '000')
