# EX for 5 Stage Pipeline

class instr_execute_5stage():
    def __init__(self, state):
        self.state = state
        self.execution_dict = {"ADD": self.ADD,
                               "SUB": self.SUB,
                               "XOR": self.XOR,
                               "OR": self.OR,
                               "AND": self.AND,
                               "ADDI": self.ADDI,
                               "XORI": self.XORI,
                               "ORI": self.ORI,
                               "ANDI": self.ANDI,
                               "JAL": self.JAL,
                               "BEQ": self.BEQ,
                               "BNE": self.BNE,
                               "LW": self.LW,
                               "SW": self.SW,
                               "HALT": self.HALT,
                               "PASS": self.PASS}


# --------------------- 5 Stage Pipeline Execution Functions -----------------------

    def ADD(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] + self.state.EX["Read_data2"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def SUB(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] - self.state.EX["Read_data2"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def XOR(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] ^ self.state.EX["Read_data2"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def OR(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] | self.state.EX["Read_data2"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def AND(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] & self.state.EX["Read_data2"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def ADDI(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] + self.state.EX["Imm"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def XORI(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] ^ self.state.EX["Imm"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def ORI(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] | self.state.EX["Imm"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def ANDI(self):
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] & self.state.EX["Imm"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def JAL(self):
        self.state.MEM["ALUresult"] = self.state.IF["PC"] - 4
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.IF["PC"] = self.state.IF["PC"] + self.state.EX["Imm"] - 8
        self.state.IF["branch"] = 1
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def BEQ(self):
        if self.state.EX["Read_data1"] == self.state.EX["Read_data2"]:
            self.state.IF["PC"] += self.state.EX["Imm"] - 8
            self.state.IF["branch"] = 1

        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def BNE(self):
        if self.state.EX["Read_data1"] != self.state.EX["Read_data2"]:
            self.state.IF["PC"] += self.state.EX["Imm"] - 8
            self.state.IF["branch"] = 1
            
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def LW(self):
        self.state.MEM["rd_mem"] = 1
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] + self.state.EX["Imm"]
        self.state.MEM["Wrt_reg_addr"] = self.state.EX["Wrt_reg_addr"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def SW(self):
        self.state.MEM["wrt_mem"] = 1
        self.state.MEM["ALUresult"] = self.state.EX["Read_data1"] + self.state.EX["Imm"]
        self.state.MEM["Store_data"] = self.state.EX["Read_data2"]
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]


    def HALT(self):
        self.state.MEM["wrt_enable"] = self.state.EX["wrt_enable"]
        self.state.EX["nop"] = float("inf")

        if self.state.WB["wrt_enable"] == 0:
            self.state.MEM["nop"] = float("inf")
            self.state.WB["nop"] = float("inf")


    def PASS(self):
        pass


# -------------------- Main Function -------------------
    def execute(self):


        if self.state.EX["nop"]:
            self.state.EX["nop"] -= 1
            return

        #resetting states
        for i_ in self.state.MEM:
            if i_ == "nop":
                continue
            self.state.MEM[i_] = 0


        self.execution_dict[self.state.EX["alu_op"]]()

    
