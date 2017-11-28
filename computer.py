import math
#
# This program simluates a basic computer by reading from
# the file "program.txt" and executing a set of basic
# instructions which result in various memory
# operations being preformed
#

class Computer:

    def __init__(self, filename):
        self.debug = False

        # init registers
        self.PC = 0 # program counter
        self.AC = 0 # accumulator register
        self.IR = 0 # instruction register

        # Load program into memory
        _memory = open(filename, 'r').read().splitlines()
        _memory = _memory[1:] # remove first row (headder)
        self.memory = [[int(y, 16) for y in x[3:].split(" ")] for x in _memory] # rem 1st col

    def get(self, address): # read from memory
        row = address // 8
        col = address % 8
        return self.memory[row][col]

    def getValue(self, address): # read value pointed by address
        value = self.get(address)
        value = self.get(value)
        return value

    def put(self, address, value): # write to memory
        row = address // 8
        col = address % 8
        if (value < 0): value = (~(-1*value)) + 1 # store in twos complement
        self.memory[row][col] = value

    def comp(self, value1, value2=None):
        if self.IR == int(value1, 16):
            return True

        if value2 != None:
            return self.IR == int(value2, 16)

        return False

    def bpad(self, value):
        s = len(value)
        return value if s == 8 else "0"*(8-s) + value

    def check(self, value):
        binary = bin(value)[2:]
        if (self.bpad(binary)[0] == "1"):
            arr = ["0" if x == "1" else "1" for x in self.bpad(binary)]
            s = "".join(arr)
            return -1 * (int(s, 2)+1)
        return value

    def add(self, a, b):
        a = self.check(a)
        b = self.check(b)
        return int((a + b) % math.pow(2, 8))

    def sub(self, a, b):
        a = self.check(a)
        b = self.check(b)
        return int((a - b) % math.pow(2, 8))

    def AND(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.getValue(self.PC)
        if (self.comp("81")): value = self.get(value) # indirect value
        if self.debug: print("  AND AC with", value)
        self.AC = self.AC & value
        if self.debug: print("  AC:", self.AC, "(" + hex(self.AC) + ")")

    def ADD(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.getValue(self.PC)
        if (self.comp("82")): value = self.get(value) # indirect value
        if self.debug: print("  ADD AC with", value, "(" + hex(value) + ")")
        self.AC = self.add(self.AC, value)
        if self.debug: print("  AC:", self.AC, "(" + hex(self.AC) + ")")

    def SUB(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.getValue(self.PC)
        if (self.comp("83")): value = self.get(value) # indirect value
        if self.debug: print("  SUB from AC with", value, "(" + hex(value) + ")")
        self.AC = self.sub(self.AC, value)
        if self.debug: print("  AC:", self.AC, "(" + hex(self.AC) + ")")

    def LDA(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.getValue(self.PC)
        if (self.comp("84")): value = self.get(value)
        if self.debug: print("  LDA AC with", value, "(" + hex(value) + ")")
        self.AC = value

    def STA(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.get(self.PC)
        if (self.comp("88")): value = self.get(value)
        if self.debug: print("  STA value", self.AC, "(" + hex(self.AC) + ")", "in loc", value, "(" + hex(value) + ")")
        self.put(value, self.AC)

    def BUN(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        value = self.get(self.PC)
        if (self.comp("90")): value = self.get(value)
        self.PC = value - 1 # because PC is incremented in run loop
        if self.debug: print("  PC:", self.PC)

    def ISZ(self):
        self.PC += 1
        if self.debug: print("  PC:", self.PC)
        address = self.get(self.PC)
        value   = self.get(address)
        res     = self.add(1, value)
        self.put(address, res)
        if (res == 0): self.PC += 2
        if self.debug: print("  INC ADDRESS:", address, "(" + hex(address) + ")")
        if self.debug: print("  RES:", res, "(" + hex(res) + ")")
        if self.debug: print("  PC:", self.PC)

    def CLA(self):
        self.AC = 0
        if self.debug: print("  AC:", self.AC, "(" + hex(self.AC) + ")")

    def CMA(self):
        self.AC = ~self.AC # ~ is bitwise complement
        if self.debug: print("  AC:", self.AC, "(" + hex(self.AC) + ")")

    def execute(self, IR):
        if (self.comp("01", "81")):   # AND
            if self.debug: print(" EXEC AND")
            self.AND()

        elif (self.comp("02", "82")): # ADD
            if self.debug: print(" EXEC ADD")
            self.ADD()

        elif (self.comp("03", "83")): # SUB
            if self.debug: print(" EXEC SUB")
            self.SUB()

        elif (self.comp("04", "84")): # LDA
            if self.debug: print(" EXEC LDA")
            self.LDA()

        elif (self.comp("08", "88")): # STA
            if self.debug: print(" EXEC STA")
            self.STA()

        elif (self.comp("10", "90")): # BUN
            if self.debug: print(" EXEC BUN")
            self.BUN()

        elif (self.comp("20", "A0")): # ISZ
            if self.debug: print(" EXEC ISZ")
            self.ISZ()

        elif (self.comp("41")): # CLA
            if self.debug: print(" EXEC CLA")
            self.CLA()

        elif (self.comp("42")): # CMA
            if self.debug: print(" EXEC CMA")
            self.CMA()

        elif (self.comp("44")): # ASL
            if self.debug: print(" EXEC ASL")
            self.ASL()

        elif (self.comp("48")): # ASR
            if self.debug: print(" EXEC ASR")
            self.ASR()

        elif (self.comp("50")): # INC
            if self.debug: print(" EXEC INC")
            self.INC()

    def pad(self, value):
        return value if len(value) == 2 else "0" + str(value)

    def dump(self, filename):

        f = open(filename, 'w')
        f.write("   +0 +1 +2 +3 +4 +5 +6 +7\n")
        line_number = "00"

        for line in self.memory:
            f.write(self.pad(line_number) + " ")

            for x in line:
                f.write(self.pad(hex(x)[2:]) + " ")

            line_number = int(str(line_number), 16) + 8
            line_number = hex(line_number)[2:]

            f.write("\n")

    def run(self):
        while(True): # program runs until halt (0x60) is encountered

            self.IR = self.get(self.PC)
            if self.debug: print("IR:", self.IR, "(" + hex(self.IR) + ")")

            if (self.comp("60")):
                if self.debug: print("HALT")
                break # program ends

            self.execute(self.IR)
            self.PC += 1
            if self.debug: print("  PC:", self.PC)


# main
computer = Computer("program.txt")
computer.run()
computer.dump("output.txt")
