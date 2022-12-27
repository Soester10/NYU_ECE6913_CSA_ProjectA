# WB for 5 Stage Pipeline


class instr_writeback_5stage():
    def __init__(self, state, myRF):
        self.state = state
        self.myRF = myRF

    # to make sure rd != 0
    def r0_check(self, rs):
        if rs == 0:
            return True
        return False

# -------------------- Main Function -------------------

    def writeback(self):

        if self.state.WB["nop"]:
            self.state.WB["nop"] -= 1
            return
        
        if self.state.WB["wrt_enable"]:
            if not self.r0_check(self.state.WB["Wrt_reg_addr"]):
                self.myRF.writeRF(self.state.WB["Wrt_reg_addr"], self.state.WB["Wrt_data"])

        if self.state.MEM["nop"] == float("inf"):
            self.state.WB["nop"] = float("inf")
