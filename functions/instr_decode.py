# Decode Instruction
from functions.instr_execute import *

class instr_decode():

    # to convert bin to int, for including the correct conversion of -ve num
    def conv_int(self, imm):
        if imm[0] == '1':       #neg
            xor_op = "0b" + ("1"* (len(imm)-1))
            imm = bin((int(imm, 2) ^ int(xor_op, 2)) + 1)[2:]

        ans = ((-1)**int(imm[0])) * int(imm[1:], 2)
        return ans
        
    
    def decode(self, state, instr, myRF):
        opcode = instr[-1:-8:-1][::-1]

        if opcode == "0110011":
            # R-Type
            rs1 = instr[-16:-21:-1][::-1]
            rs2 = instr[-21:-26:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func7 = instr[-26:-33:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_rtype = {
                ("0000000", "000"): ADD(),
                ("0100000", "000"): SUB(),
                ("0000000", "100"): XOR(),
                ("0000000", "110"): OR(),
                ("0000000", "111"): AND()
                }


            state.EX["Rs"] = rs1
            state.EX["Rt"] = rs2

            state.EX["Read_data1"] = self.conv_int(myRF.readRF(int(rs1, 2)))
            state.EX["Read_data2"] = self.conv_int(myRF.readRF(int(rs2, 2)))
            
            state.EX["Wrt_reg_addr"] = int(rd, 2)
            state.EX["wrt_enable"] = 1
            state.IF["PC"] += 4

            return ex_dict_rtype[(func7, func3)]

        elif opcode == "0010011":
            # I-Type
            rs1 = instr[-16:-21:-1][::-1]
            imm = instr[-21:-33:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_itype = {
                ("000"): ADDI(),
                ("100"): XORI(),
                ("110"): ORI(),
                ("111"): ANDI()
                }


            state.EX["Rs"] = rs1

            state.EX["Read_data1"] = self.conv_int(myRF.readRF(int(rs1, 2)))
            state.EX["Imm"] = self.conv_int(imm)
            
            state.EX["Wrt_reg_addr"] = int(rd, 2)
            state.EX["wrt_enable"] = 1
            state.EX["is_I_type"] = True
            state.IF["PC"] += 4

            return ex_dict_itype[(func3)]

        elif opcode == "1101111":
            # J-Type
            rd = instr[-8:-13:-1][::-1]
            imm1 = instr[-22:-32:-1][::-1]
            imm2 = instr[-21]
            imm3 = instr[-13:-21:-1][::-1]
            imm4 = instr[-32]
            imm = imm4 + imm3 + imm2 + imm1

            ex_dict_jtype = {
                ("1"): JAL()
                }


            state.EX["Imm"] = self.conv_int(imm) * 2
            state.EX["Wrt_reg_addr"] = int(rd, 2)
            state.EX["wrt_enable"] = 1

            return ex_dict_jtype[("1")]

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
                ("000"): BEQ(),
                ("001"): BNE(),
                }

            state.EX["Rs"] = rs1
            state.EX["Rt"] = rs2

            state.EX["Read_data1"] = self.conv_int(myRF.readRF(int(rs1, 2)))
            state.EX["Read_data2"] = self.conv_int(myRF.readRF(int(rs2, 2)))
            state.EX["Imm"] = self.conv_int(imm) * 2

            return ex_dict_btype[(func3)]

        elif opcode == "0000011":
            # Load
            rs1 = instr[-16:-21:-1][::-1]
            imm = instr[-21:-33:-1][::-1]
            rd = instr[-8:-13:-1][::-1]
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_load = {
                ("000"): LW()
                }


            state.EX["Rs"] = rs1

            state.EX["Read_data1"] = self.conv_int(myRF.readRF(int(rs1, 2)))
            state.EX["Imm"] = self.conv_int(imm)
            
            state.EX["Wrt_reg_addr"] = int(rd, 2)
            state.EX["wrt_enable"] = 1
            state.IF["PC"] += 4

            return ex_dict_load[(func3)]

        elif opcode == "0100011":
            # Store
            rs1 = instr[-16:-21:-1][::-1]
            rs2 = instr[-21:-26:-1][::-1]
            imm1 = instr[-8:-13:-1][::-1]
            imm2 = instr[-26:-33:-1][::-1]
            imm = imm2 + imm1
            
            func3 = instr[-13:-16:-1][::-1]

            ex_dict_store = {
                ("010"): SW(),
                }

            state.EX["Rs"] = rs1
            state.EX["Rt"] = rs2

            state.EX["Read_data1"] = self.conv_int(myRF.readRF(int(rs1, 2)))
            state.EX["Imm"] = self.conv_int(imm)
            state.EX["Read_data2"] = self.conv_int(myRF.readRF(int(rs2, 2)))
            
            state.IF["PC"] += 4

            return ex_dict_store[(func3)]

        else:
            # Halt
            return HALT()

        
