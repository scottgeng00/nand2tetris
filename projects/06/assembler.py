import re
import sys

class Parser:
    
    def __init__(self, path):
        f = open(path, 'r')

        self.source = []
        self.length = 0
        for line in f.readlines():
            self.source.append(line.strip())
            self.length += 1

        self.lineCounter = 0
        self.currrentLine = None
        self.currentSymbol = None

        self.L_PATTERN = re.compile(r'\(([a-zA-Z][\w:.$]+|\d+)\)')
        self.A_PATTERN = re.compile(r'@([a-zA-Z][\w:.$]+|\d+)')
        self.C_PATTERN = re.compile(r'([AMD]{0,3})=?([01\&!\|AMD+-]+);?(J[MPGTLEQN]{2})?')

    def hasMoreCommands(self):
        if self.lineCounter < self.length:
            return True
        return False

    def advance(self):
        try:
            self.currentLine = self.source[self.lineCounter]
            self.lineCounter += 1
            return self.currentLine
        except Exception as error:
            print("End of file reached: " + repr(error))

    def parse(self):
        commentless = self.currentLine.split("//")[0]
        if self.A_PATTERN.match(commentless) is not None:
            return ('A', self.A_PATTERN.findall(self.currentLine))
        
        elif self.L_PATTERN.match(commentless) is not None:
            return ('L', self.L_PATTERN.findall(self.currentLine))

        elif self.C_PATTERN.match(commentless) is not None:
            return ('C', self.C_PATTERN.findall(self.currentLine))
        else:
            return (None, None)


class SymbolTable:

    def __init__(self):
        self.table = dict()
        #prepopulate table with default entries
        self.addEntry('SP', 0); self.addEntry('LCL', 1); self.addEntry('ARG', 2)
        self.addEntry('THIS', 3); self.addEntry('THAT', 4)
        self.addEntry('SCREEN', 16384); self.addEntry('KBD', 24576)
        for i in range(0, 16):
            self.addEntry('R'+str(i), i)

    def contains(self, symbol):
        return symbol in self.table
    def addEntry(self, symbol, addr):
        self.table[symbol] = bin(int(addr))[2:].zfill(15)        #associate symbol with a 15 digit binary string
    def getAddress(self, symbol):
        if not symbol.isnumeric():
            return self.table[symbol]
        return bin(int(symbol))[2:].zfill(15)

class Code:

    def __init__(self, table: SymbolTable):
        self.sym_table = table
        self.op_chart = {                                   #hardcoding all these codes is kidna jank
            '0'  :'0101010', '1'  :'0111111',
            '-1' :'0111010', 'D'  :'0001100',
            'A'  :'0110000', '!D' :'0001101',
            '!A' :'0110001', '-D' :'0001111',
            'D+1':'0011111', 'A+1':'0110111',
            'D-1':'0001110', 'A-1':'0110010',
            'D+A':'0000010', 'D-A':'0010011',
            'A-D':'0000111', 'D&A':'0000000',
            'D|A':'0010101', 'M'  :'1110000',
            '!M' :'1110001', '-M' :'1110011',
            'M+1':'1110111', 'M-1':'1110010',
            'D+M':'1000010', 'D-M':'1010011',
            'M-D':'1000111', 'D&M':'1000000',
            'D|M':'1010101'
        }
        self.jmp_chart = {
            'JGT':'001', 'JEQ':'010', 'JGE':'011',
            'JLT':'100', 'JNE':'101', 'JLE':'110',
            'JMP':'111'
        }

    def codeA(self, command):
        addr = self.sym_table.getAddress(command)      #let the symbol table handle converting dec to binary
        return '0' + addr 
    
    def codeC(self, command):
        dest = command[0]
        op = command[1]
        jmp = command[2]

        dest_code = ['0', '0', '0']
        op_code = self.op_chart[op]
        jmp_code = '000'

        if 'A' in dest:
            dest_code[0] = '1'
        if 'D' in dest:
            dest_code[1] = '1'
        if 'M' in dest:
            dest_code[2] = '1'
        
        if jmp != '':
            jmp_code = self.jmp_chart[jmp]

        return '111' + op_code + ''.join(dest_code) + jmp_code
        


def main(path: str):
    #two-pass assembler: first pass builds the symbol table with loop labels, second pass generates codes

    #FIRST PASS
    table = SymbolTable()
    pCounter = 0                #program counter 
    rCounter = 16               #initial ram loocation for user-defined variables

    parser = Parser(path)

    while parser.hasMoreCommands():
        parser.advance()
        ctype, command = parser.parse()
        if ctype == 'A' or ctype == 'C':
            pCounter += 1
        elif ctype == 'L':
            table.addEntry(command[0], pCounter)

    #SECOND PASS
    parser = Parser(path)
    encoder = Code(table)
    bincode = []

    while parser.hasMoreCommands():
        parser.advance()
        ctype, command = parser.parse()
        if ctype == 'C':
            print(command)
            print(encoder.codeC(command[0]))
            bincode.append(encoder.codeC(command[0]))
        elif ctype == 'A':
            print(command)
            if not table.contains(command[0]) and not command[0].isnumeric():
                table.addEntry(command[0], rCounter)
                rCounter += 1
            print(encoder.codeA(command[0]))
            bincode.append(encoder.codeA(command[0]))
    
    print("\n")

    outpath = path[:-3] + 'hack'
    out = open(outpath, 'w')
    for line in bincode:
        print(line)
        out.write(line + "\n")

    out.close()

if __name__ == "__main__" :
    path = "./test.asm"
    
    if len(sys.argv) > 1:
        path = sys.argv[1]

    main(path)


    
    
