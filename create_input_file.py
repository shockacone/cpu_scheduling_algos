import random, math, sys

NUM_PROCS        = 50
CTX_SWITCH_TICKS = 5
MEAN_ARRIVAL     = 50.0
MEAN_BURSTS      = 20
CPU_MIN, CPU_MAX = 5,500
IO_MIN,  IO_MAX  = 30,1000
SEED             = 42

random.seed(SEED)

def next_exp(mean):
    return int(random.expovariate(1 / mean) + 0.5)

def bounded_rnd(lo, hi):
    return random.randint(lo, hi)

out = sys.stdout
print(NUM_PROCS, CTX_SWITCH_TICKS, file=out)

clock = 0
for pid in range(1, NUM_PROCS + 1):

    clock += next_exp(MEAN_ARRIVAL)
    bursts = max(1, int(random.gauss(MEAN_BURSTS, MEAN_BURSTS/3)))
    print(pid, clock, bursts, file=out)

    for i in range(1, bursts):
        cpu = bounded_rnd(CPU_MIN, CPU_MAX)
        io  = bounded_rnd(IO_MIN,  IO_MAX)
        print(i, cpu, io,        file=out)

    cpu_last = bounded_rnd(CPU_MIN, CPU_MAX)
    print(bursts, cpu_last,     file=out)

