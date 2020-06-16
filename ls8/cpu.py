"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter, index of the current instruction 
        self.reg = [0] * 8 # 8 registers / like variables 
        self.ram = [0] * 256 #ram
        self.branchtable ={}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul

    def ram_read(self, MDR ): # accept the address to read and return the value stored 
        return self.ram[MDR]

    def ram_write(self, val, MDR): # accept a value to write, and the address to write it to 
        self.ram[MDR] = val

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        address = 0
        with open(filename) as filehandle:
            for line in filehandle:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                # self.ram[address] = v
                self.ram_write(v, address)
                address += 1
    
    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc +=3

    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc +1)])
        self.pc += 2

    def handle_mul(self):
        reg_1 = self.ram_read(self.pc + 1)
        reg_2 = self.ram_read(self.pc + 2)
        prod = self.reg[reg_1] * self.reg[reg_2]
        self.reg[reg_1] = prod
        self.pc += 3

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def add(self, operand_a=None, operand_b=None):
        self.alu("ADD", operand_a, operand_b)

    def run(self):
        """Run the CPU."""
        ir = LDI
        self.branchtable[ir]()
        ir = LDI
        self.branchtable[ir]()
        ir = MUL
        self.branchtable[ir]()
        ir = PRN
        self.branchtable[ir]()
        
