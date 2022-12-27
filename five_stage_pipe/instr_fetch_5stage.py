# IF for 5 Stage Pipeline

class instr_fetch_5stage():
    def __init__(self, state, imem):
        self.state = state
        self.imem = imem

    def fetch(self):

        if self.state.IF["nop"]:
            self.state.IF["nop"] -= 1
            return

        #resetting states
        for i_ in self.state.ID:
            if i_ == "nop":
                continue
            self.state.ID[i_] = 0
        
        instr = self.imem.readInstr(self.state.IF["PC"])
        self.state.ID["Instr"] = instr
        self.state.IF["PC"] += 4
        self.state.IF["branch"] = 0
        self.state.IF["add_1"] = 0


        #check for HALT
        opcode = self.state.ID["Instr"][-1:-8:-1][::-1]

        if opcode not in ["0110011", "0010011", "1101111", "1100011", "0000011", "0100011"]:
            if (self.state.EX["wrt_enable"] == 0 and self.state.EX["wrt_mem"] == 0)\
               and (self.state.MEM["wrt_enable"] == 0 and self.state.MEM["wrt_mem"] == 0)\
               and self.state.WB["wrt_enable"] == 0:
                return

            self.state.IF["add_1"] = 1

        

        


