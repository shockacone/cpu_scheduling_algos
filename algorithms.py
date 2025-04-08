import os, sys
from classes import Process, CPU_burst

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

def SJF_preemptive (process_list):

    all_bursts_empty = 0
    process_ran = 0
    event = 0
    cpu_free = True
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])

    #print(max_arrival_time, " ", min_arrival_time)
    #burst_using_cpu = None

    while all_bursts_empty == 0:
        processes_to_consider = []

        if event < max_arrival_time:
            for process in process_list:
                if event >= process.arrival_time:
                    processes_to_consider.append(process)
        elif event >= max_arrival_time:
            processes_to_consider = process_list

        sorted_process_and_valid_burst_list = [(sorted_tuple[0],sorted_tuple[1]) for sorted_tuple in
                sorted([(process, process.find_valid_cpu_burst(), process.find_valid_cpu_burst().cpu_time) for process in processes_to_consider], key=lambda x: x[2])]
        duplicate_shortest_time = 0 
        duplicate_count = 0
        shortest_time = 0
        shortest_p_and_b = False

        for process_and_burst in sorted_process_and_valid_burst_list:
            if process_and_burst[1].cpu_time >= 0 and shortest_time == 0:
                     shortest_p_and_b = process_and_burst
                     shortest_time = shortest_p_and_b[1].cpu_time

            elif shortest_time > 0 and process_and_burst[1].cpu_time == shortest_time and duplicate_count != 0:
                #HERE if there are duplicate shortest bursts, loop through the processes and bursts (in sorted_process_and_valid_burst_list) and find the process and burst that arrived at the earliest time (by process arrival time). Give the CPU to that process/burst and continue to the next iteration
                duplicate_shortest_time += 1
                print(process_and_burst)
                print(shortest_p_and_b)
            duplicate_count += 1

        if duplicate_shortest_time >= 1:
            print("DUPLICATE SHORTEST TIME!")

        #print(sorted_process_and_valid_burst_list)
        if event < min_arrival_time:
            print(event)
        else:
            for process_and_burst in sorted_process_and_valid_burst_list:
                process = process_and_burst[0]
                burst = process_and_burst[1]
                
                #testing
                cc = 0
                if cpu_free:
                    cc = 1
                cpu_free = process_burst(burst, cpu_free)
                
                if cc == 1 and not cpu_free:
                    print(f"{process.process_index}, {burst}, Event time: {event}")

                burst_using_cpu = burst
                process_using_cpu = process.process_index

                if burst.cpu_time == 0 and (burst.io_time == 0 or burst.io_time == -1):
                    if burst.is_empty != 1:
                        burst.time_finished = event + 1
                        print(f"{process.process_index}, {burst.burst_index}, {burst.time_finished} burst is finished.")
                        burst.is_empty = 1

        if burst_using_cpu:
            if burst_using_cpu.cpu_time <= 0:
                burst_using_cpu = None
                process_using_cpu = None

        cpu_free = True

        if max([process.calc_total_time_left() for process in process_list]) <= 0:
            all_bursts_empty = 1
        
        event += 1
        if event == 10000:
            break

    for process in process_list:
        process.calc_time_finished()
        print(f"Process {process.process_index} finished at time {process.time_finished}.")
        print(process)

def SJF_non_preemptive (process_list):

    all_bursts_empty = 0
    process_ran = 0
    event = 0
    cpu_free = True
    max_arrival_time = max([process.arrival_time for process in process_list])
    min_arrival_time = min([process.arrival_time for process in process_list])

    #print(max_arrival_time, " ", min_arrival_time)
    burst_using_cpu = None

    while all_bursts_empty == 0:
        processes_to_consider = []

        if event < max_arrival_time:
            for process in process_list:
                if event >= process.arrival_time:
                    processes_to_consider.append(process)
        elif event >= max_arrival_time:
            processes_to_consider = process_list

        sorted_process_and_valid_burst_list = [(sorted_tuple[0],sorted_tuple[1]) for sorted_tuple in
                sorted([(process, process.find_valid_cpu_burst(), process.find_valid_cpu_burst().cpu_time) for process in processes_to_consider], key=lambda x: x[2])]
        #print(sorted_process_and_valid_burst_list)


        #print(sorted_process_and_valid_burst_list)
        if event < min_arrival_time:
            print(event)
        else:
            #print(burst_using_cpu, cpu_free)
            for process_and_burst in sorted_process_and_valid_burst_list:
                #print(process_and_burst[0].process_index, process_and_burst[1])
                process = process_and_burst[0]
                burst = process_and_burst[1]

                #print(burst_using_cpu, cpu_free, burst)
                if burst is burst_using_cpu or (burst_using_cpu is None and cpu_free == True and burst.cpu_time >= 1):
                    #print("USING CPU")
                    cpu_free = process_burst(burst, cpu_free)
                    burst_using_cpu = burst
                    process_using_cpu = process.process_index
                    #continue
                elif burst.is_empty != 1 and burst.cpu_time <= 0 and not (burst_using_cpu is burst):
                    cpu_free = process_burst(burst, cpu_free)

                if burst.cpu_time == 0 and (burst.io_time == 0 or burst.io_time == -1):
                    if burst.is_empty != 1:
                        burst.time_finished = event + 1
                        print(f"{process.process_index}, {burst.burst_index}, {burst.time_finished} burst is finished.")
                        burst.is_empty = 1


        #print(f"Process: {process_using_cpu}, {burst_using_cpu}, {event}")

        if burst_using_cpu:
            if burst_using_cpu.cpu_time <= 0:
                burst_using_cpu = None
                process_using_cpu = None

        cpu_free = True

        if max([process.calc_total_time_left() for process in process_list]) <= 0:
            all_bursts_empty = 1
        
        event += 1
        if event == 10000:
            break

    for process in process_list:
        process.calc_time_finished()
        print(f"Process {process.process_index} finished at time {process.time_finished}.")
        print(process)

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


