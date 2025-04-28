import os, sys
from classes import Process, CPU_burst
import re
import miscellaneous
import algorithms
import argument_handling
import copy

def main():
    argument_dict = argument_handling.handle_arguments()
    context_switch = 0

    #print(argument_dict)

    if argument_dict['input_file']:
        process_list, context_switch = miscellaneous.return_process_list(argument_dict['input_file'])
        argument_dict['context_switch'] = context_switch
    else:
        print("Input file not specified! Please give an input file. Use '-h' for the help menu.")
        sys.exit()

    #This is just a band-aid. I should be making copies of the objects themselves in the algorithms and using those but for now I don't want to change the algorithm code-base too much.
    second_process_list = [copy.deepcopy(o) for o in process_list]
    third_process_list = [copy.deepcopy(o) for o in process_list]
    fourth_process_list = [copy.deepcopy(o) for o in process_list]

    if argument_dict['a'] == 'FCFS':
        algorithms.event_based_FCFS(process_list, argument_dict)
    elif argument_dict['a'] == 'SJF':
        algorithms.SJF_non_preemptive(second_process_list, argument_dict)
    elif argument_dict['a'] == 'SRTN':
        algorithms.SJF_preemptive(third_process_list, argument_dict)
    elif argument_dict['a'] == 'RR':
        algorithms.RR(fourth_process_list, argument_dict)
    elif not argument_dict['a']:
        algorithms.event_based_FCFS(process_list, argument_dict)
        algorithms.SJF_non_preemptive(second_process_list, argument_dict)
        algorithms.SJF_preemptive(third_process_list, argument_dict)
        algorithms.RR(fourth_process_list, argument_dict)

if __name__ == "__main__":
    main()

