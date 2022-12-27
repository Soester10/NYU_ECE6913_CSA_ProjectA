# ID for 5 Stage Pipeline

class instr_decode_5stage():

    def __init__(self, state, myRF, imem):
        self.state = state
        self.myRF = myRF
        self.imem = imem
        self.ins_list = []


    def resolve_hazard(self, rs):
        if rs == 0:
            rs = self.myRF.readRF(rs)
            rs = int(rs, 2)
            return rs

        #resolving branch control flow
        if self.state.IF["branch"]:         #branch taken as PC is changed
            self.state.ID["nop"] += 1         # discarding this ins, then next IF will get the branch
            self.state.EX["alu_op"] = "PASS"
            
        
        #EX/ID Forwarding
        elif rs == self.state.MEM["Wrt_reg_addr"] and self.state.EX["alu_op"]!="LW":
            rs = self.state.MEM["ALUresult"]

        #Load-Use Data Hazard
        elif rs == self.state.MEM["Wrt_reg_addr"] and self.state.EX["alu_op"]=="LW":
            #insert nops for all following stages in this cycle, since hazard cannot be resolved
            self.state.ID["nop"] += 1
            self.state.IF["nop"] += 1

        #MEM/ID Forwarding
        elif rs == self.state.WB["Wrt_reg_addr"]:
            rs = self.state.WB["Wrt_data"]

        else:
            rs = self.myRF.readRF(rs)
            rs = self.conv_int(rs)

        return rs


    def conv_int(self, imm):
        if imm[0] == '1':       #neg
            xor_op = "0b" + ("1"* (len(imm)-1))
            imm = bin((int(imm, 2) ^ int(xor_op, 2)) + 1)[2:]

        ans = ((-1)**int(imm[0])) * int(imm[1:], 2)
        return ans    
            

    def decode(self):

        if self.state.ID["nop"]:
            self.state.ID["nop"] -= 1
            return

        #resetting states
        for i_ in self.state.EX:
            if i_ == "nop" or i_ == "alu_op":
                continue
            self.state.EX[i_] = 0

        # ----------------- 5 Stage Pipeline Decode -------------------

        opcode = self.state.ID["Instr"][-1:-8:-1][::-1]

        instr = self.state.ID["Instr"]

        if opcode == "0110011":
            # R-Type
            rs1 = instr[-16:-21:-1][::-1]
            rs2 = instr[-21:-26:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func7 = instr[-26:-33:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_rtype = {
                ("0000000", "000"): "ADD",
                ("0100000", "000"): "SUB",
                ("0000000", "100"): "XOR",
                ("0000000", "110"): "OR",
                ("0000000", "111"): "AND"
                }

            temp1 = rs1
            temp2 = rs2
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)

            rs1 = self.resolve_hazard(rs1)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return
            
            rs2 = self.resolve_hazard(rs2)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return

            self.state.EX["Rs"] = temp1
            self.state.EX["Rt"] = temp2
            self.state.EX["Read_data1"] = rs1
            self.state.EX["Read_data2"] = rs2
            self.state.EX["Wrt_reg_addr"] = int(rd, 2)
            self.state.EX["wrt_enable"] = 1
            self.state.EX["alu_op"] = ex_dict_rtype[(func7, func3)]

        elif opcode == "0010011":
            # I-Type
            rs1 = instr[-16:-21:-1][::-1]
            imm = instr[-21:-33:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_itype = {
                ("000"): "ADDI",
                ("100"): "XORI",
                ("110"): "ORI",
                ("111"): "ANDI"
                }

            temp1 = rs1
            rs1 = int(rs1, 2)

            rs1 = self.resolve_hazard(rs1)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return

            self.state.EX["Rs"] = temp1
            self.state.EX["Read_data1"] = rs1
            self.state.EX["Imm"] = self.conv_int(imm)
            self.state.EX["Wrt_reg_addr"] = int(rd, 2)
            self.state.EX["wrt_enable"] = 1
            self.state.EX["is_I_type"] = True
            self.state.EX["alu_op"] = ex_dict_itype[(func3)]

        elif opcode == "1101111":
            # J-Type
            rd = instr[-8:-13:-1][::-1]
            imm1 = instr[-22:-32:-1][::-1]
            imm2 = instr[-21]
            imm3 = instr[-13:-21:-1][::-1]
            imm4 = instr[-32]
            imm = imm4 + imm3 + imm2 + imm1

            ex_dict_jtype = {
                ("1"): "JAL"
                }

            #resolving branch control flow
            if self.state.IF["branch"]:     #branch taken as PC is changed
            # discarding this ins, then next IF will get the branch
                self.state.EX["alu_op"] = "PASS"
                return

            self.state.EX["Imm"] = self.conv_int(imm) * 2
            self.state.EX["Wrt_reg_addr"] = int(rd, 2)
            self.state.EX["wrt_enable"] = 1
            self.state.EX["alu_op"] = ex_dict_jtype[("1")]

        elif opcode == "1100011":
            # B-Type
            rs1 = instr[-16:-21:-1][::-1]
            rs2 = instr[-21:-26:-1][::-1]
            
            imm1 = instr[-9:-13:-1][::-1]
            imm2 = instr[-26:-32:-1][::-1]
            imm3 = instr[-8]
            imm4 = instr[-32]
            imm = imm4 + imm3 + imm2 + imm1

            func3 = instr[-13:-16:-1][::-1]

            ex_dict_btype = {
                ("000"): "BEQ",
                ("001"): "BNE",
                }

            temp1 = rs1
            temp2 = rs2
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)

            rs1 = self.resolve_hazard(rs1)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return
            
            rs2 = self.resolve_hazard(rs2)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return

            self.state.EX["Rs"] = temp1
            self.state.EX["Rt"] = temp2
            self.state.EX["Read_data1"] = rs1
            self.state.EX["Read_data2"] = rs2
            self.state.EX["Imm"] = self.conv_int(imm) * 2
            self.state.EX["alu_op"] = ex_dict_btype[(func3)]
            self.state.EX["wrt_enable"] = 0

        elif opcode == "0000011":
            # Load
            rs1 = instr[-16:-21:-1][::-1]
            imm = instr[-21:-33:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_load = {
                ("000"): "LW",
                }

            temp1 = rs1
            rs1 = int(rs1, 2)
            
            rs1 = self.resolve_hazard(rs1)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return

            self.state.EX["Rs"] = temp1
            self.state.EX["Read_data1"] = rs1
            self.state.EX["Imm"] = self.conv_int(imm)
            self.state.EX["Wrt_reg_addr"] = int(rd, 2)
            self.state.EX["wrt_enable"] = 1
            self.state.EX["alu_op"] = ex_dict_load[(func3)]

        elif opcode == "0100011":
            # Store
            rs1 = instr[-16:-21:-1][::-1]
            rs2 = instr[-21:-26:-1][::-1]
            imm1 = instr[-8:-13:-1][::-1]
            imm2 = instr[-26:-33:-1][::-1]
            imm = imm2 + imm1
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_store = {
                ("010"): "SW",
                }

            temp1 = rs1
            temp2 = rs2
            rs1 = int(rs1, 2)
            rs2 = int(rs2, 2)

            rs1 = self.resolve_hazard(rs1)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return
            
            rs2 = self.resolve_hazard(rs2)
            if self.state.ID["nop"]:
                self.state.ID["nop"] -= 1
                return

            self.state.EX["Rs"] = temp1
            self.state.EX["Rt"] = temp2
            self.state.EX["Read_data1"] = rs1
            self.state.EX["Imm"] = self.conv_int(imm)
            self.state.EX["Read_data2"] = rs2
            self.state.EX["alu_op"] = ex_dict_store[(func3)]
            self.state.EX["wrt_enable"] = 0
            self.state.EX["rd_mem"] = 0


        else:
            # Halt
            #resolving branch control flow
            if self.state.IF["branch"]:     #branch taken as PC is changed
            # discarding this ins, then next IF will get the branch
                self.state.EX["alu_op"] = "PASS"
                return
            
            self.state.EX["alu_op"] = "HALT"
            self.state.IF["nop"] = float("inf")
            self.state.ID["nop"] = float("inf")
            self.state.EX["nop"] = float("inf")

            if self.state.MEM["wrt_enable"] == 0 and self.state.MEM["wrt_mem"] == 0:
                self.state.MEM["nop"] = float("inf")

                if self.state.WB["wrt_enable"] == 0:
                    self.state.WB["nop"] = float("inf")


        
            
        
