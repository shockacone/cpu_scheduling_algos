import argparse
import yaml
import sys


def handle_arguments():
    parser = argparse.ArgumentParser(prog='sim.py',
            description="This is an event-driven simulator for CPU algorithms.",
            epilog='Example:\nsim.py -a FCFS --input_file <input_file>',
            formatter_class=argparse.RawDescriptionHelpFormatter
            )


    #sim [-d][-v][-a algorithm] < input_ile
    #-d stands for detailed information
    #-v stands for verbose mode
    #-a stands for the execution of a given algorithm (constrained to valid inputs)
    parser.add_argument('-d', '--detailed', action='store_true', help="detailed information")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode")
    parser.add_argument('-a', type=str, help="Algorithm selection")
    parser.add_argument('--input_file', type=str, help="Input file for processes. To create an input file, do 'python create_input_file.py > example_file'")
    parser.add_argument('-q', '--time_quantum', type=int, help="Time quantum for RR algorithm.")
    
    args = parser.parse_args()
    args_dict = vars(args)

    return args_dict
