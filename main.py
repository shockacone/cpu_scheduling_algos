import os, sys
from classes import Process, CPU_burst
import re
import miscellaneous
import algorithms

def main():
    #print("Arguments:", sys.argv)

    process_list = miscellaneous.return_process_list(sys.argv[1])
    for proc in process_list:
        #print(proc)
        pass

    #algorithms.event_based_FCFS(process_list)
    #algorithms.SJF_non_preemptive(process_list)
    algorithms.SJF_preemptive(process_list)

if __name__ == "__main__":
    main()

