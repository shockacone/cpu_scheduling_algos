import os, sys

#default mode output
def default_mode(sorted_event_queue, alg_completion_time, cpu_util, process_list, algorithm_name):
    
    print('')
    print(f"{algorithm_name}:")
    print (f"Total Time required is: {alg_completion_time} units")
    print (f"CPU Utilization is {cpu_util}%")

#detailed information mode (-d)
def detailed_mode(sorted_event_queue, alg_completion_time, cpu_util, process_list):

    print('')
    for i in process_list:
        print(f"Process {i.process_index}")
        print(f"Arrival time: {i.arrival_time}")
        print(f"Service time: {i.service_time} units")
        print(f"I/O time: {i.total_io_time} units")
        print(f"Turnaround time: {i.turnaround_time} units")
        print(f"Finish time: {i.time_finished} units")

#verbose mode (-v)
def verbose_mode(sorted_event_queue, alg_completion_time, cpu_util, process_list):

    print('')
    for i in sorted_event_queue:
        print(i)

'''
Write a 2-3 page paper describing your project, what problems you've faced and how you've overcome them. In your
opinion, what is the best scheduling algorithm? What are practical limitations on that algorithm?
What is the effect of decreasing context switch time to 1 time unit? What is the effect of increasing it to 10? What
percentage of turnaround time is the process waiting?
'''

'''
What to submit:
Submit your test data.
Submit ALL source code with detailed instructions on how and where to compile it, and how to make it run. You should
submit a Makefile to build your code under GCC/G++ (recommended), Java, or whatever language you use. Note that Visual
C++ also supports Makefiles, so if you use that, you can still export a makefile. I will test some of the code to make sure the
numbers are not imagined.
Submit traces of execution (the trace of execution of each algorithm; each algorithm in separate files, etc.). 
Submit your findings about each algorithm; average numbers (waiting times, etc.) (in addition to your 2-3 page paper)
Submit your paper describing the project.
Submit a file named: description.txt that describes what and where all the information is stored. (which file does what, which
file contains results of which algorithm, etc.). This is mostly so that I don't get lost in your project directory.
Note: All descriptions and text should be in TEXT format. Do NOT submit MS Word documents, etc. Everything has to be
readable without any special programs. (If something "has" to be formated, use PDF).
You may use any language you wish, but you need to document what language you're using and how to compile code
somewhere in your submission. Also comment your code! If I can't read it, it's wrong! 
'''
