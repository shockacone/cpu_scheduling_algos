import os, sys
from classes import Process, CPU_burst
import re

def return_process_list(input_file):
    
    process_list = []
    first_line = 0
    process_line_count = 0

    with open(input_file, 'r') as file:
        for line in file:
            if len(re.split(' ', line)) > 3:
                print("Unrecognized line!! Exiting...")
                sys.exit()

            if first_line != 0:
                #print (line)
                if process_line_count == 0:
                    #print("This line is to instantiate a process.")
                    input_line = [int(x) for x in re.split(' ', line)]
                    process = Process(input_line[0], input_line[1], input_line[2])
                    process_line_count = input_line[2]

                else:
                    #print("This line is to instantiate a cpu burst.")
                    input_line = [int(x) for x in re.split(' ', line)]
                    if (process_line_count == 1):
                        cpu_burst = CPU_burst(input_line[0], input_line[1], -1)
                        process_list.append(process)
                    else:
                        cpu_burst = CPU_burst(input_line[0], input_line[1], input_line[2])
                    process.add_cpu_burst(cpu_burst)
                    process_line_count -= 1
                    assert(process_line_count >= 0)


            elif first_line == 0 and len(re.split(' ', line)) == 2:
                #print("This is the first line. It includes the number of processes and the time for a process switch.")
                first_line += 1

            else:
                print("Unrecognized first line of input file!! The first line must provide ONLY 'number_of_processes' and 'process_switch'. Exiting...")
                sys.exit()

    return process_list
