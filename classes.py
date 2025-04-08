import os
import sys

class CPU_burst:
    def __init__(self, burst_index, cpu_time, io_time):
        self.burst_index = burst_index
        self.cpu_time = cpu_time
        self.io_time = io_time
        self.is_empty = 0
        self.is_waiting = False
        self.total_waiting = 0
        self.time_finished = -1

    def __repr__(self):
        return f"CPU_burst(index={self.burst_index}, cpu={self.cpu_time}, io={self.io_time}, finished={self.time_finished})"

class Process:
    def __init__(self, process_index, arrival_time, cpu_burst_num):
        self.process_index = process_index
        self.arrival_time = arrival_time
        self.cpu_burst_num = cpu_burst_num
        self.cpu_bursts = []
        self.service_time = 0
        self.cpu_burst_combined_time = 0
        #self.io_time = 0
        self.io_wait = False
        self.turnaround_time = 0
        self.time_finished = 0 
        self.is_empty = 0

    def add_cpu_burst(self, cpu_burst: CPU_burst):
        if len(self.cpu_bursts) >= self.cpu_burst_num:
            raise OverflowError("Buffer is full")
        self.cpu_bursts.append(cpu_burst)

    def calc_time_finished(self):
        for burst in self.cpu_bursts:
            if self.time_finished <= burst.time_finished:
                self.time_finished = burst.time_finished
    
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
            
    def find_valid_cpu_burst(self):
        not_blocked = 1
        valid_burst = self.cpu_bursts[0]

        for burst in self.cpu_bursts:
            if burst.cpu_time == 0 and burst.io_time <= 0:
                pass
            else:
                return burst

        return self.cpu_bursts[len(self.cpu_bursts) - 1]

    def __repr__(self):
        return (f"Process(index={self.process_index}, arrival={self.arrival_time}, "
                f"bursts={self.cpu_burst_num}, cpu_bursts={self.cpu_bursts}), "
                f"total_cpu_time={self.cpu_burst_combined_time}")

