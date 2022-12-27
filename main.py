import os
import argparse
from functions.instr_decode import instr_decode
from five_stage_pipe.instr_fetch_5stage import instr_fetch_5stage
from five_stage_pipe.instr_decode_5stage import instr_decode_5stage
from five_stage_pipe.instr_execute_5stage import instr_execute_5stage
from five_stage_pipe.instr_memory_5stage import instr_memory_5stage
from five_stage_pipe.instr_writeback_5stage import instr_writeback_5stage
from functions.generate_metrics import Generate_Metrics


MemSize = 1000

# memory size, in reality, the memory size should be 2^32,
#but for this lab, for the space resaon, we keep it as this large number,
#but the memory is still 32-bit addressable.


# Class to convert int to binary, for including the correct conversion of -ve num
class Conv_Bin():
    def conv_bin(self, WriteData_binary):
        xor_op = "0b" + ("1"* (len(WriteData_binary)))
        WriteData_binary = bin((int(WriteData_binary, 2) ^ int(xor_op, 2)) + 1)[2:]

        return WriteData_binary



class InsMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        
        with open(os.path.join(ioDir, "imem.txt")) as im:
            self.IMem = [data.replace("\n", "") for data in im.readlines()]

    def readInstr(self, ReadAddress):
        #read instruction memory
        return ''.join(self.IMem[ReadAddress: ReadAddress+4])
          


class DataMem(object):
    def __init__(self, name, ioDir):
        self.id = name
        self.ioDir = ioDir
        with open(os.path.join(ioDir, "dmem.txt")) as dm:
            self.DMem = [data.replace("\n", "") for data in dm.readlines()]

        # MemSize = 1000 lines
        self.DMem = self.DMem + ["0" * 8 for i in range(MemSize - len(self.DMem))]

    def readInstr(self, ReadAddress):
        #read data memory
        return ''.join(self.DMem[ReadAddress: ReadAddress+4])
        
    def writeDataMem(self, Address, WriteData):
        #check for neg and do 2s complement
        msb = 0
        if WriteData < 0:
            msb = 1
            WriteData = abs(WriteData)
        
        # write data into byte addressable memory
        WriteData_binary = bin(WriteData)[2:][:32]
        pad = "0" * (32 - len(WriteData_binary))
        WriteData_binary = pad + WriteData_binary         #padding

        if msb:
            WriteData_binary = Conv_Bin().conv_bin(WriteData_binary)
            
        WriteData_list = [WriteData_binary[i*8: (i*8)+8] for i in range(4)]
        self.DMem[Address: Address+4] = WriteData_list[:]
        
    def outputDataMem(self):
        resPath = os.path.join(self.ioDir, self.id + "_DMEMResult.txt")
        with open(resPath, "w") as rp:
            rp.writelines([str(data) + "\n" for data in self.DMem])
            


class RegisterFile(object):
    def __init__(self, ioDir):
        self.outputFile = ioDir + "RFResult.txt"
        self.Registers = ['0'* 32 for i in range(32)]
    
    def readRF(self, Reg_addr):
        return self.Registers[Reg_addr]
    
    def writeRF(self, Reg_addr, Wrt_reg_data):
        #check for neg and do 2s complement
        msb = 0
        if Wrt_reg_data < 0:
            msb = 1
            Wrt_reg_data = abs(Wrt_reg_data)
        
        Wrt_reg_data = bin(Wrt_reg_data)[2:][:32]
        pad = "0" * (32 - len(Wrt_reg_data))
        Wrt_reg_data = pad + Wrt_reg_data         #padding

        if msb:
            Wrt_reg_data = Conv_Bin().conv_bin(Wrt_reg_data)

        self.Registers[Reg_addr] = Wrt_reg_data
         
    def outputRF(self, cycle):
        op = ["-"*70+"\n", "State of RF after executing cycle:" + str(cycle) + "\n"]
        op.extend([str(val)+"\n" for val in self.Registers])
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.outputFile, perm) as file:
            file.writelines(op)



class State(object):
    def __init__(self):

        self.IF = {"nop": False,
                   "PC": 0,
                   "branch": False,
                   "add_1": 0}

        self.ID = {"nop": False,
                   "Instr": 0}

        self.EX = {"nop": False,
                   "Read_data1": 0,
                   "Read_data2": 0,
                   "Imm": 0,
                   "Rs": 0,
                   "Rt": 0,
                   "Wrt_reg_addr": 0,
                   "is_I_type": False,
                   "rd_mem": 0,
                   "wrt_mem": 0,
                   "alu_op": 0,
                   "wrt_enable": 0}
        
        self.MEM = {"nop": False,
                    "ALUresult": 0,
                    "Store_data": 0,
                    "Rs": 0,
                    "Rt": 0,
                    "Wrt_reg_addr": 0,
                    "rd_mem": 0,
                    "wrt_mem": 0,
                    "wrt_enable": 0}
        
        self.WB = {"nop": False,
                   "Wrt_data": 0,
                   "Rs": 0,
                   "Rt": 0,
                   "Wrt_reg_addr": 0,
                   "wrt_enable": 0}
        



class Core(object):
    def __init__(self, ioDir, imem, dmem):
        self.myRF = RegisterFile(ioDir)
        self.cycle = 0
        self.halted = False
        self.ioDir = ioDir
        self.state = State()
        self.nextState = State()
        self.ext_imem = imem
        self.ext_dmem = dmem



class SingleStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(SingleStageCore, self).__init__(os.path.join(ioDir, "SS_"), imem, dmem)
        self.opFilePath = os.path.join(ioDir, "StateResult_SS.txt")

    def step(self):

        # Single Stage: 1 Cycle/ Ins: All stages are executed one after the other for each ins

        # IF
        instr = self.ext_imem.readInstr(self.state.IF["PC"])

        # ID
        self.state.ID["Instr"] = instr
        ex_func = instr_decode().decode(self.state, instr, self.myRF)

        # EX
        ex_func.execute(self.state)

        #MEM
        ex_func.memory(self.state, self.ext_dmem)

        #WB
        if self.state.WB["Wrt_reg_addr"] != 0 and self.state.WB["wrt_enable"]:
            self.myRF.writeRF(self.state.WB["Wrt_reg_addr"], self.state.WB["Wrt_data"])


        # Retaining the PC for extracting next ins
        next_PC = self.state.IF["PC"]

        if self.state.IF["nop"]:
            if self.state.IF["add_1"] == 0:
                self.halted = True
            self.state.IF["add_1"] = 0
            
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.state, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 
            
        self.state = self.nextState #The end of the cycle and updates the current state with the values calculated in this cycle
        self.state.IF["PC"] = next_PC       # Retaining the PC for extracting next ins
        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.append("IF.PC: " + str(state.IF["PC"]) + "\n")
        printstate.append("IF.nop: " + str(state.IF["nop"]) + "\n")
        
        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)




class FiveStageCore(Core):
    def __init__(self, ioDir, imem, dmem):
        super(FiveStageCore, self).__init__(os.path.join(ioDir, "FS_"), imem, dmem)
        self.opFilePath = os.path.join(ioDir, "StateResult_FS.txt")

    def step(self):

        if self.cycle == 0:
            self.state.IF["nop"] = 0
            self.state.ID["nop"] = 1
            self.state.EX["nop"] = 2
            self.state.MEM["nop"] = 3
            self.state.WB["nop"] = 4

       
        # --------------------- WB stage ---------------------

        instr_writeback_5stage(self.state, self.myRF).writeback()
        
        # --------------------- MEM stage --------------------
        
        instr_memory_5stage(self.state, self.ext_dmem).memory()
        
        # --------------------- EX stage ---------------------
        
        instr_execute_5stage(self.state).execute()
        
        # --------------------- ID stage ---------------------
        
        instr_decode_5stage(self.state, self.myRF, self.ext_imem).decode()
        
        # --------------------- IF stage ---------------------
        
        instr_fetch_5stage(self.state, self.ext_imem).fetch()

        # --------------------- -- ----- ---------------------


        if self.state.IF["nop"] and self.state.ID["nop"] and self.state.EX["nop"] and self.state.MEM["nop"] and self.state.WB["nop"]:
            if self.state.IF["add_1"] == 0:
                self.halted = True
            self.state.IF["add_1"] = 0
        
        self.myRF.outputRF(self.cycle) # dump RF
        self.printState(self.state, self.cycle) # print states after executing cycle 0, cycle 1, cycle 2 ... 

        self.cycle += 1

    def printState(self, state, cycle):
        printstate = ["-"*70+"\n", "State after executing cycle: " + str(cycle) + "\n"]
        printstate.extend(["IF." + key + ": " + str(val) + "\n" for key, val in state.IF.items()])
        printstate.extend(["ID." + key + ": " + str(val) + "\n" for key, val in state.ID.items()])
        printstate.extend(["EX." + key + ": " + str(val) + "\n" for key, val in state.EX.items()])
        printstate.extend(["MEM." + key + ": " + str(val) + "\n" for key, val in state.MEM.items()])
        printstate.extend(["WB." + key + ": " + str(val) + "\n" for key, val in state.WB.items()])

        if(cycle == 0): perm = "w"
        else: perm = "a"
        with open(self.opFilePath, perm) as wf:
            wf.writelines(printstate)



# Main

if __name__ == "__main__":
     
    #parse arguments for input file location
    parser = argparse.ArgumentParser(description='RV32I processor')
    parser.add_argument('--iodir', default="", type=str, help='Directory containing the input files.')
    args = parser.parse_args()

    ioDir = os.path.abspath(args.iodir)
    print("IO Directory:", ioDir)

    imem = InsMem("Imem", ioDir)
    dmem_ss = DataMem("SS", ioDir)
    dmem_fs = DataMem("FS", ioDir)
    
    ssCore = SingleStageCore(ioDir, imem, dmem_ss)
    fsCore = FiveStageCore(ioDir, imem, dmem_fs)

    while(True):
        if not ssCore.halted:
            ssCore.step()
        
        if not fsCore.halted:
            fsCore.step()

        if ssCore.halted and fsCore.halted:
            break
    
    # dump SS and FS data mem.
    dmem_ss.outputDataMem()
    dmem_fs.outputDataMem()

    #genrate mertics file for ss
    Generate_Metrics().generate("w", "Metrics for SS:", ssCore.cycle, ssCore.cycle-1, ioDir)

    #genrate mertics file for fs
    Generate_Metrics().generate("a", "Metrics for FS:", fsCore.cycle, ssCore.cycle-1, ioDir)
