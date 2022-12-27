# Execute Instruction


# R- Types
# ADD Class
class ADD():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] + state.EX["Read_data2"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]



# SUB Class
class SUB():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] - state.EX["Read_data2"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# XOR Class
class XOR():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] ^ state.EX["Read_data2"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# OR Class
class OR():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] | state.EX["Read_data2"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# AND Class
class AND():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] & state.EX["Read_data2"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]




# I-Types
# ADDI Class
class ADDI():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] + state.EX["Imm"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# XORI Class
class XORI():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] ^ state.EX["Imm"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# ORI Class
class ORI():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] | state.EX["Imm"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]


# ANDI Class
class ANDI():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] & state.EX["Imm"]
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]




# J-Types
# JAL Class
class JAL():
    def execute(self, state):
        state.MEM["ALUresult"] = state.IF["PC"] + 4
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.IF["PC"] += state.EX["Imm"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = state.MEM["ALUresult"]
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]




# B-Types
# BEQ Class
class BEQ():
    def execute(self, state):
        if state.EX["Read_data1"] == state.EX["Read_data2"]:
            state.IF["PC"] += state.EX["Imm"]
        else:
            state.IF["PC"] += 4

    def memory(self, state, dmem):
        pass



# BNE Class
class BNE():
    def execute(self, state):
        if state.EX["Read_data1"] != state.EX["Read_data2"]:
            state.IF["PC"] += state.EX["Imm"]
        else:
            state.IF["PC"] += 4

    def memory(self, state, dmem):
        pass



# Load Type
# LW Class
class LW():
    def conv_int(self, imm):
        if imm[0] == '1':       #neg
            xor_op = "0b" + ("1"* (len(imm)-1))
            imm = bin((int(imm, 2) ^ int(xor_op, 2)) + 1)[2:]

        ans = ((-1)**int(imm[0])) * int(imm[1:], 2)
        return ans
    
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] + state.EX["Imm"]
        state.MEM["rd_mem"] = 1
        state.MEM["Wrt_reg_addr"] = state.EX["Wrt_reg_addr"]
        state.MEM["wrt_enable"] = state.EX["wrt_enable"]

    def memory(self, state, dmem):
        state.WB["Wrt_data"] = self.conv_int(dmem.readInstr(state.MEM["ALUresult"]))
        state.WB["Wrt_reg_addr"] = state.MEM["Wrt_reg_addr"]
        state.WB["wrt_enable"] = state.MEM["wrt_enable"]



# Store Type
# SW Class
class SW():
    def execute(self, state):
        state.MEM["ALUresult"] = state.EX["Read_data1"] + state.EX["Imm"]
        state.MEM["wrt_mem"] = 1
        state.MEM["Store_data"] = state.EX["Read_data2"]

    def memory(self, state, dmem):
        dmem.writeDataMem(state.MEM["ALUresult"], state.MEM["Store_data"])



# HALT Class
class HALT():
    def execute(self, state):
        if not state.IF["nop"]:
            state.IF["add_1"] = 1
        state.IF["nop"] = True

    def memory(self, state, dmem):
        pass

