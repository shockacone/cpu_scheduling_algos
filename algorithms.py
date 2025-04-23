import os, sys
from classes import Process, CPU_burst, Event

def process_burst(cpu_burst, cpu_free):
    if cpu_free == True and cpu_burst.cpu_time != 0:
        cpu_burst.cpu_time -= 1
        cpu_free = False

    elif cpu_free == True and cpu_burst.cpu_time == 0 and cpu_burst.io_time >= 1:
        cpu_burst.is_waiting = False
        cpu_burst.io_time -= 1
        #cpu_free = False

    elif cpu_free != True and cpu_burst.cpu_time != 0:
        cpu_burst.is_waiting = True
        cpu_burst.total_waiting += 1

    elif cpu_free != True and cpu_burst.cpu_time == 0 and cpu_burst.io_time >= 1:
        cpu_burst.is_waiting = False
        cpu_burst.io_time -= 1

    return cpu_free

def preemptive_sjf_process_burst(shortest_and_arrived, event_time, next_arrival_time, event_queue, process_list):

    #So we will get the process and the burst
    #We will need to compare the differences in cpu_times between valid bursts
    #Valid bursts are given to us by a method from the processes
    #so Maybe we can iterate through the processes and get the next time for which a burst will arrive or for which a 'ready' burst will have cpu time which is shorter than the current one. So next event time could be the minumum of the difference between next arrival time and current time or cpu_time remaining.

    #tuple of process and burst
    current_tuple = shortest_and_arrived
    burst = current_tuple[1]
    process = current_tuple[0]
    cpu_time = burst.cpu_time
    io_time = burst.io_time

    if burst.execution_starts == -1:
        burst.execution_starts = event_time
    
    #print(burst, process)
    #If a previous process was running and it no longer is selected as having the shortest burst, change its state from 'running' to 'ready'
    for proc in process_list:
        if proc is process:
            pass
        elif proc.state == 'running':
            event_queue.append(Event(event_time, proc, proc.state, 'ready'))

    next_arrived = 0
    cpu_remaining = 0

    if next_arrival_time > event_time:
        if next_arrival_time - event_time >= cpu_time:
            burst.end_time = event_time + cpu_time + io_time
            burst_counter = 0

            if burst.execution_starts == event_time:
                event_queue.append(Event(event_time, process, process.state, 'ready'))

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
        else:
            diff = next_arrival_time - event_time
            burst.cpu_time -= diff 

            if process.state != 'running':
                event_queue.append(Event(event_time, process, process.state, 'running'))

            event_time += diff

            #event_queue.append(Event(event_time, process, process.state, 'ready'))
            return event_time
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


def SJF_preemptive (process_list):

    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    cpu_idle_time = min_arrival_time 

    for process in process_list:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    while not all_bursts_empty:
        processes_to_consider = []
        processes_to_consider = process_list
        process_and_valid_burst_list = []
        
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, valid_burst)
                process_and_valid_burst_list.append(process_and_burst)

        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].cpu_time)
        #next_arrival_time = sorted_process_and_valid_burst_list[0][1].arrival_time
        by_arrival = sorted(process_and_valid_burst_list, key=lambda x: x[1].arrival_time)
        not_arrived = []

        for process_and_burst in by_arrival:
            if process_and_burst[1].arrival_time > event_time:
                not_arrived.append(process_and_burst)

        shortest_and_arrived = []
        for process_and_burst in sorted_process_and_valid_burst_list:
            if process_and_burst[1].arrival_time <= event_time: 
                shortest_and_arrived.append(process_and_burst)

        next_arrival_time = -1

        if not_arrived:
            next_arrival_time = not_arrived[0][1].arrival_time

        #if shortest_and_arrived:
            #print(event_time, shortest_and_arrived[0][1])

        #print(f"event_time = {event_time}, ", f"next_arrival = {next_arrival_time}, ", shortest_and_arrived[0][0].process_index, shortest_and_arrived[0][1])
        if shortest_and_arrived:
            event_time = preemptive_sjf_process_burst(shortest_and_arrived[0], event_time, next_arrival_time, event_queue, process_list)
        else:
            if next_arrival_time != -1:
                cpu_idle_time += next_arrival_time - event_time
                event_time = next_arrival_time
            else:
                print("arrival_time is -1 and there is no process that is ready, something is wrong.")
                sys.exit()

        #print(event_time)
        #print(f"Total time left at least: {max([process.calc_total_time_left() for process in process_list])}")
        if max([process.calc_total_time_left() for process in process_list]) <= 0:
            all_bursts_empty = 1
            time_finished = 0
            for process in process_list:
                if max([burst.end_time for burst in process.cpu_bursts]) > time_finished:
                    time_finished = max([burst.end_time for burst in process.cpu_bursts])
                    
            print(f"All bursts have been processed at time: {time_finished}")
            print(f"CPU idle time is: {cpu_idle_time}")

    burst_process_list = [(burst, process) for process in process_list for burst in process.cpu_bursts]
    sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    #for i in sorted_burst_process_list:
    #    print(f"Process: {i[1].process_index}, {i[0]}\n")
    
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)
    for i in sorted_event_queue:
        print(i)

def SJF_non_preemptive (process_list):

    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    cpu_idle_time = min_arrival_time 

    for process in process_list:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    while not all_bursts_empty:
        processes_to_consider = []
        processes_to_consider = process_list
        process_and_valid_burst_list = []
        
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, process.find_valid_cpu_burst(event_time))
                process_and_valid_burst_list.append(process_and_burst)

        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].cpu_time)
        #next_arrival_time = sorted_process_and_valid_burst_list[0][1].arrival_time
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
            event_time = non_preemptive_process_burst(shortest_and_arrived[0], event_time, event_queue)
        else:
            cpu_idle_time += next_arrival_time - event_time
            event_time = next_arrival_time

        #print(f"Total time left at least: {max([process.calc_total_time_left() for process in process_list])}")
        if max([process.calc_total_time_left() for process in process_list]) <= 0:
            all_bursts_empty = 1
            print(f"All bursts have been processed at time: {event_time}")

    burst_process_list = [(burst, process) for process in process_list for burst in process.cpu_bursts]
    sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    for i in sorted_burst_process_list:
        print(f"Process: {i[1].process_index}, {i[0]}\n")
    
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)
    for i in sorted_event_queue:
        print(i)

def non_preemptive_process_burst(process_and_burst, event_time, event_queue):
    process = process_and_burst[0]
    burst = process_and_burst[1]

    burst.execution_starts = event_time
    cpu_time = burst.cpu_time
    io_time = burst.io_time
    burst.end_time = event_time + cpu_time + io_time
    event_time = burst.execution_starts + burst.cpu_time
    
    burst_counter = 0

    event_queue.append(Event(burst.arrival_time, process, process.state, 'ready'))
    event_queue.append(Event(burst.execution_starts, process, process.state, 'running'))

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
    
    print(burst)
    return event_time

def event_based_FCFS(process_list):
    event_queue = []
    event_time = 0
    cpu_free = True
    all_bursts_empty = 0
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])
    event_time = min_arrival_time

    cpu_idle_time = 0

    for process in process_list:
        process.cpu_bursts[0].arrival_time = process.arrival_time

    while not all_bursts_empty:
        processes_to_consider = []
        processes_to_consider = process_list
        process_and_valid_burst_list = []
        
        for process in processes_to_consider:
            valid_burst = process.find_valid_cpu_burst(event_time)
            if valid_burst:
                process_and_burst = (process, process.find_valid_cpu_burst(event_time))
                process_and_valid_burst_list.append(process_and_burst)

        sorted_process_and_valid_burst_list = sorted(process_and_valid_burst_list, key=lambda x: x[1].arrival_time)
        next_arrival_time = sorted_process_and_valid_burst_list[0][1].arrival_time

        if event_time >= next_arrival_time:
            event_time = non_preemptive_process_burst(sorted_process_and_valid_burst_list[0], event_time, event_queue)
        else:
            cpu_idle_time += next_arrival_time - event_time
            event_time = next_arrival_time

        #print(f"Total time left at least: {max([process.calc_total_time_left() for process in process_list])}")
        if max([process.calc_total_time_left() for process in process_list]) <= 0:
            all_bursts_empty = 1
            print(f"All bursts have been processed at time: {event_time}")

    burst_process_list = [(burst, process) for process in process_list for burst in process.cpu_bursts]
    sorted_burst_process_list = sorted(burst_process_list, key=lambda x:x[0].execution_starts)

    for i in sorted_burst_process_list:
        print(f"Process: {i[1].process_index}, {i[0]}\n")
    
    sorted_event_queue = sorted(event_queue, key = lambda x:x.event_time)
    for i in sorted_event_queue:
        print(i)

def FCFS (process_list):
    event_queue = []
    event = 0
    cpu_free = True
    is_process_io_blocked = 0

    for process in process_list:
        while process.is_empty == 0:
            process_ran = 0
            for burst_counter in range(len(process.cpu_bursts)):
                #check if burst is IO blocked by previous burst (process will wait on IO before proceeding)
                for secondary_burst_counter in range(burst_counter):
                    #print(secondary_burst_counter)
                    if process.cpu_bursts[secondary_burst_counter].io_time != 0:
                        is_process_io_blocked = 1

                if process.cpu_bursts[burst_counter].cpu_time == 0 and (process.cpu_bursts[burst_counter].io_time == 0 or process.cpu_bursts[burst_counter].io_time == -1):
                    if process.cpu_bursts[burst_counter].is_empty != 1:
                        process.cpu_bursts[burst_counter].time_finished = event
                        process.cpu_bursts[burst_counter].is_empty = 1

                if process.cpu_bursts[burst_counter].is_empty != 1 and is_process_io_blocked == 0:
                    cpu_free = process_burst(process.cpu_bursts[burst_counter], cpu_free)
                    process_ran = 1
                    break

                print(process.cpu_bursts[burst_counter], cpu_free)
            bursts_empty = []
            for burst_counter in range(len(process.cpu_bursts)):
                if process.cpu_bursts[burst_counter].is_empty == 1:
                    #process.is_empty = 1
                    bursts_empty.append(1)
                else:
                    bursts_empty.append(0)

            if min(bursts_empty) == 1:
                process.is_empty = 1

            if process_ran == 1:
                event += 1
            else:
                event += 5

            cpu_free = True
            is_process_io_blocked = 0

    for process in process_list:
        process.calc_time_finished()
        print(f"Process {process.process_index} finished at time {process.time_finished}.")
        print(process)


