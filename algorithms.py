import os, sys
from classes import Process, CPU_burst, Event
import output_handler 


def preemptive_sjf_process_burst(shortest_and_arrived, event_time, next_arrival_time, event_queue, process_list, context_switch):

    #This is the method which processes each burst for preemptive algorithms (ignore the sjf in the name). In each preemptive algorithm, once a CPU burst is chosen as the next one to be processed, this method is called to handle that.
    #tuple of process and burst
    current_tuple = shortest_and_arrived
    burst = current_tuple[1]
    process = current_tuple[0]
    cpu_time = burst.cpu_time
    io_time = burst.io_time

    #Is there a context switch? Look for previous event and see if a different process was in 'running' or 'terminated' state
    previous_running_event = False
    switching_context = False

    for i in event_queue:
        #find the most recent event for which there was a process in the running state
        if i.previous_state == 'running':
            previous_running_event = i     
    
    #if there was a different process that came out of the running state, there is a context switch
    if previous_running_event:
        if previous_running_event.process.process_index != process.process_index:
            switching_context = True
            event_time += context_switch

    if burst.execution_starts == -1:
        burst.execution_starts = event_time
    
    #If a previous process was running and it no longer is selected as having the shortest burst, change its state from 'running' to 'ready'
    for proc in process_list:
        if proc is process:
            pass
        elif proc.state == 'running':
            event_queue.append(Event(event_time, proc, proc.state, 'ready'))

    next_arrived = 0
    cpu_remaining = 0

    #This if statement is to figure out if I'm bounded by a burst that is arriving shortly.
    if next_arrival_time > event_time:
        #If this burst is bounded by an arrival time which does not enable it to complete, perform the following actions...
        if next_arrival_time - event_time >= cpu_time:
            burst.end_time = event_time + cpu_time + io_time
            burst_counter = 0

            if burst.execution_starts == event_time:
                event_queue.append(Event(event_time, process, process.state, 'ready'))
                #There may be a context switch here

            if process.state != 'running':
                event_queue.append(Event(event_time, process, process.state, 'running'))

            for cpu_burst in process.cpu_bursts:
                if cpu_burst is burst and burst_counter < len(process.cpu_bursts) - 1:
                    process.cpu_bursts[burst_counter+1].arrival_time = burst.end_time
                    event_queue.append(Event(event_time + cpu_time, process, process.state, 'blocked'))
                elif cpu_burst is burst:
                    event_queue.append(Event(burst.end_time, process, process.state, 'terminated'))

                burst_counter += 1

            event_time += burst.cpu_time
            burst.cpu_time = 0
            burst.io_time = 0
            burst.is_empty = 1
            
            #print(burst)
            return event_time
        #If this burst is not bounded by an incoming burst and the cpu time can complete, proceed as usual
        else:
            diff = next_arrival_time - event_time
            burst.cpu_time -= diff 

            if process.state != 'running':
                event_queue.append(Event(event_time, process, process.state, 'running'))

            event_time += diff

            #event_queue.append(Event(event_time, process, process.state, 'ready'))
            return event_time
    #If there are no upcoming bursts to deal with, we will execute this burst until completion
    else:
        if process.state != 'running':
            event_queue.append(Event(event_time, process, process.state, 'running'))

        burst.end_time = event_time + cpu_time + io_time
        burst_counter = 0

        for cpu_burst in process.cpu_bursts:
            if cpu_burst is burst and burst_counter < len(process.cpu_bursts) - 1:
                process.cpu_bursts[burst_counter+1].arrival_time = burst.end_time
                event_queue.append(Event(event_time + cpu_time, process, process.state, 'blocked'))
            elif cpu_burst is burst:
                event_queue.append(Event(burst.end_time, process, process.state, 'terminated'))

            burst_counter += 1

        event_time += burst.cpu_time
        burst.cpu_time = 0
        burst.io_time = 0
        burst.is_empty = 1

        #print(burst)
        return event_time


def RR (process_list, argument_dict):
    
    alg_completion_time = 0
    cpu_util = 0
    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    #Here we ensure a value for the time quantum
    if argument_dict['time_quantum']:
        time_quantum = argument_dict['time_quantum']
    else:
        time_quantum = 10
    
    next_event_time = min_arrival_time
    cpu_idle_time = min_arrival_time 

    processes_to_consider = []
    processes_to_consider = process_list
    
    #here we calculate service and IO Time
    for i in processes_to_consider:
        i.calc_service_time()
        i.calc_IO_time()

    #here we set the arrival time for the initial cpu burst of every process
    for process in processes_to_consider:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    while not all_bursts_empty:
        processes_and_bursts_left = []
        not_arrived = []

        event_processed = 0

        #starting here we try to implement the details of RR
        for process in processes_to_consider:
            process_burst = process.find_valid_cpu_burst(event_time)

            p_and_b = (process, process_burst)

            if process_burst != False:
                if process_burst.arrival_time <= event_time:
                    event_time = preemptive_sjf_process_burst(p_and_b, event_time, event_time + time_quantum, event_queue, processes_to_consider, argument_dict['context_switch'])
                    event_processed = 1
        
        if event_processed == 0:
            if max([process.calc_total_time_left() for process in processes_to_consider]) <= 0:
                all_bursts_empty = 1
                alg_completion_time = event_time
                cpu_util = float(( alg_completion_time - cpu_idle_time ) / alg_completion_time) * 100
            else:
                cpu_idle_time += time_quantum
                #next_event_time += event_time + time_quantum
                event_time += time_quantum

    #here we calculate total time it took to finish the process and its turnaround time
    for i in processes_to_consider:
        i.calc_time_finished()
        i.calc_turnaround_time()

    #here we sort the event queue for chronological printing of events
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)

    alg_name = f"Round Robin with Time Quantum {time_quantum}"

    #here we handle output printing
    output_handler.default_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider, alg_name)
    if argument_dict['detailed']:
        output_handler.detailed_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)
    if argument_dict['verbose']:
        output_handler.verbose_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)


def SJF_preemptive (process_list, argument_dict):

    alg_completion_time = 0
    cpu_util = 0
    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    cpu_idle_time = min_arrival_time 

    processes_to_consider = []
    processes_to_consider = process_list
    
    #calculate some initial values for each process
    for i in processes_to_consider:
        i.calc_service_time()
        i.calc_IO_time()

    #here we set initial arrivals for the first cpu burst in each process
    for process in processes_to_consider:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    while not all_bursts_empty:
        process_and_valid_burst_list = []
        
        #here we filter bursts based on whether they have a valid arrival time and if their predecessor burst has finished already
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, valid_burst)
                process_and_valid_burst_list.append(process_and_burst)

        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].cpu_time)
        #Here we differentiate between valid bursts and valid bursts that have already arrived. Both are useful in upcoming logic
        by_arrival = sorted(process_and_valid_burst_list, key=lambda x: x[1].arrival_time)
        not_arrived = []

        #Here we pic out those valid bursts which have not arrived
        for process_and_burst in by_arrival:
            if process_and_burst[1].arrival_time > event_time:
                not_arrived.append(process_and_burst)

        #And those that have arrived
        shortest_and_arrived = []
        for process_and_burst in sorted_process_and_valid_burst_list:
            if process_and_burst[1].arrival_time <= event_time: 
                shortest_and_arrived.append(process_and_burst)

        next_arrival_time = -1

        if not_arrived:
            next_arrival_time = not_arrived[0][1].arrival_time

        if shortest_and_arrived:
            event_time = preemptive_sjf_process_burst(shortest_and_arrived[0], event_time, next_arrival_time, event_queue, processes_to_consider, argument_dict['context_switch'])
        else:
            if next_arrival_time != -1:
                cpu_idle_time += next_arrival_time - event_time
                event_time = next_arrival_time
            else:
                print("arrival_time is -1 and there is no process that is ready, something is wrong.")
                sys.exit()

        #Here we are trying to figure out if all processes are finished already
        if max([process.calc_total_time_left() for process in processes_to_consider]) <= 0:
            all_bursts_empty = 1
            #time_finished = 0
            alg_completion_time = event_time
            cpu_util = float(( alg_completion_time - cpu_idle_time ) / alg_completion_time) * 100

    
    #burst_process_list = [(burst, process) for process in processes_to_consider for burst in process.cpu_bursts]
    #sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    #Sort the event queue for printing verbose output
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)
    #calculate some more attributes for each process
    for i in processes_to_consider:
        i.calc_time_finished()
        i.calc_turnaround_time()

    alg_name = "Shortest Remaining Time Next"
    output_handler.default_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider, alg_name)
    if argument_dict['detailed']:
        output_handler.detailed_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)
    if argument_dict['verbose']:
        output_handler.verbose_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)

def SJF_non_preemptive (process_list, argument_dict):

    alg_completion_time = 0
    cpu_util = 0
    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    cpu_idle_time = min_arrival_time 

    processes_to_consider = []
    processes_to_consider = process_list

    #calulate service and IO time for each process
    for i in processes_to_consider:
        i.calc_service_time()
        i.calc_IO_time()

    #initialize arrival time for the first burst of each process
    for process in processes_to_consider:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    #start teh implementation of non-preempt SJF
    while not all_bursts_empty:
        process_and_valid_burst_list = []
        
        #here we are figuring out which cpu bursts are valid
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, process.find_valid_cpu_burst(event_time))
                process_and_valid_burst_list.append(process_and_burst)

        #Here we are figuring out which valid bursts have the soonest arrival time and which are shortest
        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].cpu_time)
        by_arrival = sorted(process_and_valid_burst_list, key=lambda x: x[1].arrival_time)

        shortest_and_arrived = []
        for process_and_burst in sorted_process_and_valid_burst_list:
            if process_and_burst[1].arrival_time <= event_time: 
                shortest_and_arrived.append(process_and_burst)

        next_arrival_time = -1

        if not shortest_and_arrived:
            next_arrival_time = by_arrival[0][1].arrival_time
        else:
            for i in by_arrival:
                if i is shortest_and_arrived[0]:
                    pass
                else:
                    next_arrival_time = i[1].arrival_time
                    break

        if shortest_and_arrived:
            #Here we call the non-preemptive implementation of burst processing (event processing for a burst)
            event_time = non_preemptive_process_burst(shortest_and_arrived[0], event_time, event_queue, argument_dict['context_switch'])
        else:
            cpu_idle_time += next_arrival_time - event_time
            event_time = next_arrival_time

        #here we are checking if all bursts have completed
        if max([process.calc_total_time_left() for process in processes_to_consider]) <= 0:
            all_bursts_empty = 1
            alg_completion_time = event_time
            cpu_util = float(( alg_completion_time - cpu_idle_time ) / alg_completion_time) * 100
            #print(f"All bursts have been processed at time: {event_time}")

    #burst_process_list = [(burst, process) for process in processes_to_consider for burst in process.cpu_bursts]
    #sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    #sorting the event queue for verbose output    
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)

    #calculating some more figures for each process
    for i in processes_to_consider:
        i.calc_time_finished()
        i.calc_turnaround_time()

    alg_name = "Shortest Job First"
    #handling printing of each output type
    output_handler.default_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider, alg_name)
    if argument_dict['detailed']:
        output_handler.detailed_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)
    if argument_dict['verbose']:
        output_handler.verbose_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)


#This is the implementation of a non-preemptive burst event
def non_preemptive_process_burst(process_and_burst, event_time, event_queue, context_switch):
    process = process_and_burst[0]
    burst = process_and_burst[1]

    #Is there a context switch? Look for previous event and see if a different process was in 'running' or 'terminated' state
    previous_running_event = False
    switching_context = False

    for i in event_queue:
        #find the most recent event for which there was a process in the running state
        if i.previous_state == 'running':
            previous_running_event = i     
    
    #if there was a different process that came out of the running state, there is a context switch
    if previous_running_event:
        if previous_running_event.process.process_index != process.process_index:
            switching_context = True
            event_time += context_switch

    burst.execution_starts = event_time
    cpu_time = burst.cpu_time
    io_time = burst.io_time
    burst.end_time = event_time + cpu_time + io_time
    event_time = burst.execution_starts + burst.cpu_time
    
    burst_counter = 0

    #adding the appropriate events into the queue
    event_queue.append(Event(burst.arrival_time, process, process.state, 'ready'))
    event_queue.append(Event(burst.execution_starts, process, process.state, 'running'))

    #Ensuring that we mark the process as either blocked or terminated at burst completion time
    for cpu_burst in process.cpu_bursts:
        if cpu_burst is burst and burst_counter < len(process.cpu_bursts) - 1:
            process.cpu_bursts[burst_counter+1].arrival_time = burst.end_time
            event_queue.append(Event(burst.execution_starts + cpu_time, process, process.state, 'blocked'))
        elif cpu_burst is burst:
            event_queue.append(Event(burst.execution_starts + cpu_time, process, process.state, 'terminated'))

        burst_counter += 1

    burst.cpu_time = 0
    burst.io_time = 0
    burst.is_empty = 1
    
    return event_time

#Implementation of event_based FCFS algorithm
def event_based_FCFS(process_list, argument_dict):

    processes_to_consider = []
    processes_to_consider = process_list

    alg_completion_time = 0
    cpu_util = 0
    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in processes_to_consider])
    min_arrival_time = min([process.arrival_time for process in processes_to_consider])
    event_time = min_arrival_time

    cpu_idle_time = 0

    #calculating some initial figures for processes
    for i in processes_to_consider:
        i.calc_service_time()
        i.calc_IO_time()
    
    #initializing first burst arrival times for each process
    for process in processes_to_consider:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    #implementing the core of FCFS
    while not all_bursts_empty:
        process_and_valid_burst_list = []
        
        #Finding valid bursts to consider
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, process.find_valid_cpu_burst(event_time))
                process_and_valid_burst_list.append(process_and_burst)

        #sorting valid bursts by arrival time
        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].arrival_time)
        #picking out the next arriving burst
        next_arrival_time = sorted_process_and_valid_burst_list[0][1].arrival_time

        #logic for deciding what to do based on the next arrival time and where it sits in the timeline
        if event_time >= next_arrival_time:
            event_time = non_preemptive_process_burst(sorted_process_and_valid_burst_list[0], event_time, event_queue, argument_dict['context_switch'])
        else:
            cpu_idle_time += next_arrival_time - event_time
            event_time = next_arrival_time

        #here we're figuring out if all bursts have completed already
        if max([process.calc_total_time_left() for process in processes_to_consider]) <= 0:
            all_bursts_empty = 1
            alg_completion_time = event_time
            cpu_util = float(( alg_completion_time - cpu_idle_time ) / alg_completion_time) * 100

    #burst_process_list = [(burst, process) for process in processes_to_consider for burst in process.cpu_bursts]
    #sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    #final calculations for processes. prepping for output handling
    for i in processes_to_consider:
        i.calc_time_finished()
        i.calc_turnaround_time()

    #sorting the event queue in a chronological order
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)

    alg_name = "First Come First Serve"
    #handling different types of output modes
    output_handler.default_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider, alg_name)
    if argument_dict['detailed']:
        output_handler.detailed_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)
    if argument_dict['verbose']:
        output_handler.verbose_mode(sorted_event_queue, alg_completion_time, cpu_util, processes_to_consider)

