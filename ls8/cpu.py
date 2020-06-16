"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program counter, index of the current instruction 
        self.reg = [0] * 8 # 8 registers / like variables 
        self.ram = [0] * 256 #ram

    def ram_read(self, MDR ): # accept the address to read and return the value stored 
        return self.ram[MDR]

    def ram_write(self, val, MDR): # accept a value to write, and the address to write it to 
        self.ram[MDR] = val

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        running = True

        while running:

            IR = self.ram_read(self.pc)
            register_1 = self.ram_read(self.pc + 1)
            register_2 = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False
                # self.pc +=1
            elif IR == LDI:
                self.reg[register_1] = register_2
                self.pc +=3
            elif IR == PRN:
                print(self.reg[register_1])
                self.pc +=2
            else:
                print(f"bad input: {bin(IR)}")
                running = False 
        
