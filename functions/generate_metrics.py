# to generate metrics file

import os


class Generate_Metrics():
    def generate(self, perm, head_cont, cycles, tot_ins, ioDir):
        file_path = os.path.join(ioDir, "PerformanceMetrics_Result.txt")

        content = [head_cont + "\n",
                   "Number of cycles taken: " + str(cycles) + "\n",
                   "Cycles per instruction: " + str(round(cycles/ tot_ins, 2)) + "\n",
                   "Instructions per cycle: " + str(round(tot_ins/ cycles, 2)) + "\n\n"]
        
        with open(file_path, perm) as wf:
            wf.writelines(content)
        
