# MEM for 5 Stage Pipeline

class instr_memory_5stage():
    def __init__(self, state, dmem):
        self.state = state
        self.dmem = dmem

    # to convert bin to int, for including the correct conversion of -ve num
    def conv_int(self, imm):
        if imm[0] == '1':       #neg
            xor_op = "0b" + ("1"* (len(imm)-1))
            imm = bin((int(imm, 2) ^ int(xor_op, 2)) + 1)[2:]

        ans = ((-1)**int(imm[0])) * int(imm[1:], 2)
        return ans

# -------------------- Main Function -------------------

    def memory(self):

        if self.state.MEM["nop"]:
            self.state.MEM["nop"] -= 1
            return

        #resetting states
        for i_ in self.state.WB:
            if i_ == "nop":
                continue
            self.state.WB[i_] = 0
        

        if self.state.MEM["rd_mem"] != 0:
            self.state.WB["Wrt_data"] = self.conv_int(self.dmem.readInstr(self.state.MEM["ALUresult"]))
            self.state.WB["Wrt_reg_addr"] = self.state.MEM["Wrt_reg_addr"]
            self.state.WB["wrt_enable"] = self.state.MEM["wrt_enable"]

        elif self.state.MEM["wrt_mem"] != 0:
            self.dmem.writeDataMem(self.state.MEM["ALUresult"], self.state.MEM["Store_data"])
            self.state.WB["wrt_enable"] = self.state.MEM["wrt_enable"]

        else:
            self.state.WB["Wrt_data"] = self.state.MEM["ALUresult"]
            self.state.WB["Wrt_reg_addr"] = self.state.MEM["Wrt_reg_addr"]
            self.state.WB["wrt_enable"] = self.state.MEM["wrt_enable"]

        if self.state.EX["nop"] == float("inf"):
            self.state.MEM["nop"] = float("inf")
            if self.state.WB["wrt_enable"] == 0 and self.state.MEM["wrt_mem"] == 0:
                self.state.WB["nop"] = float("inf")

