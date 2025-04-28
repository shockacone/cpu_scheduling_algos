import os
import sys

class CPU_burst:
    def __init__(self, burst_index, cpu_time, io_time):
        self.burst_index = burst_index
        self.cpu_time = cpu_time
        self.io_time = io_time
        self.is_empty = False 
        self.is_waiting = False
        self.total_waiting = 0
        self.time_finished = -1
        self.execution_starts = -1 
        self.arrival_time = -1
        self.end_time = 0

    def __repr__(self):
        return f"CPU_burst(index={self.burst_index}, cpu={self.cpu_time}, io={self.io_time}, arrived={self.arrival_time}, execution_start={self.execution_starts}, finished={self.end_time})"

class Process:
    def __init__(self, process_index, arrival_time, cpu_burst_num):
        self.process_index = process_index
        self.arrival_time = arrival_time
        self.cpu_burst_num = cpu_burst_num
        self.cpu_bursts = []
        self.service_time = 0
        self.cpu_burst_combined_time = 0
        self.total_io_time = 0
        self.io_wait = False
        self.turnaround_time = 0
        self.time_finished = 0 
        self.is_empty = 0
        self.state = 'new'

    def calc_service_time(self):
        for i in self.cpu_bursts:
            self.service_time += i.cpu_time

    def calc_IO_time(self):
        for i in self.cpu_bursts:
            self.total_io_time +=i.io_time

    def calc_turnaround_time(self):
        self.turnaround_time = self.time_finished - self.arrival_time

    def add_cpu_burst(self, cpu_burst: CPU_burst):
        if len(self.cpu_bursts) >= self.cpu_burst_num:
            raise OverflowError("Buffer is full")
        self.cpu_bursts.append(cpu_burst)

    def calc_time_finished(self):
        for burst in self.cpu_bursts:
            if self.time_finished <= burst.end_time:
                self.time_finished = burst.end_time
    
    def calc_total_cpu_time(self):
        self.cpu_burst_combined_time = 0
        for burst in self.cpu_bursts:
            self.cpu_burst_combined_time += burst.cpu_time

        return self.cpu_burst_combined_time

    def calc_total_time_left(self):
        total_time_left = 0
        for i in self.cpu_bursts:
            if i.io_time != -1:
                total_time_left += i.cpu_time + i.io_time
            else:
                total_time_left += i.cpu_time

        return total_time_left
            
    def find_valid_cpu_burst(self, event_time):
        not_blocked = 1
        valid_burst = self.cpu_bursts[0]

        for burst_counter in range(len(self.cpu_bursts)):
            if burst_counter == 0:
                if self.cpu_bursts[burst_counter].cpu_time > 0 and self.cpu_bursts[burst_counter].arrival_time != -1:
                    #and (not check_arrival or self.cpu_bursts[burst_counter].arrival_time >= event_time):
                    return self.cpu_bursts[burst_counter]
            else:
                if self.cpu_bursts[burst_counter].cpu_time > 0 and self.cpu_bursts[burst_counter].arrival_time != -1 and self.cpu_bursts[burst_counter - 1].cpu_time == 0 and self.cpu_bursts[burst_counter - 1].io_time == 0:
                    #and (not check_arrival or self.cpu_bursts[burst_counter].arrival_time >= event_time):
                    #and self.cpu_bursts[burst_counter - 1].end_time < event_time:
                    return self.cpu_bursts[burst_counter]

        return False

        #return self.cpu_bursts[len(self.cpu_bursts) - 1]

    def __repr__(self):
        return (f"Process(index={self.process_index}, arrival={self.arrival_time}, "
                f"bursts={self.cpu_burst_num}, cpu_bursts={self.cpu_bursts}, "
                f"total_cpu_time={self.cpu_burst_combined_time})")

class Event:

    def __init__(self, time, process, previous_state, new_state):
        self.process = process
        #self.burst = burst
        self.event_time = time
        #self.cpu_free = cpu_free
        self.previous_state = previous_state
        self.new_state = new_state
        self.process.state = new_state

    def update_process_state (self, process):
        process.state = new_state
        

        #the five states are 'new', 'ready', 'running', 'blocked', or 'terminated'
    def __repr__(self):
        return (f"At time {self.event_time}: Process {self.process.process_index} moves from {self.previous_state} to {self.new_state}")
