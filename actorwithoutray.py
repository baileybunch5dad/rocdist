from multiprocessing import Process, Queue
import time
import sys
from DynamicDist import DynamicDist
import os
import numpy

# read from queue in multiple threads
def dynamicdist_reader(qq):
    dd = DynamicDist()
    print(f'Started {os.getpid()=} {sys.executable=} {sys.argv=}')
    n = 0
    while True:
        msg = qq.get()  
        if type(msg) == numpy.ndarray:
            n += 1
            dd.add_many(msg)
        elif type(msg) == str:
            if msg == "DONE":
                print(f'Received DONE Terminating {os.getpid()=} {sys.executable=} {sys.argv=}')
                break
        else:
            print(f"Unknown message type {type(msg)=}")

    print(f'Received {n} messages at {os.getpid()=} {sys.executable=} {sys.argv=}')
    h,b = dd.histogram(n_bins=10)
    print(f'{h=} {b=}')


def dynamicdist_writer(numcalls: int = 10000, num_processors: int = 0 , qq : Queue = None):
    """Write integers into the queue.  A reader_proc() will read them from the queue"""
    for ii in range(0, numcalls):
        qq.put(numpy.random.random(size=10000))  # Put 'count' numbers into queue

    ### Tell all readers to stop...
    for ii in range(0, num_processors):
        qq.put("DONE")


def start_reader_procs(qq: Queue, num_of_reader_procs: int) -> list:
    """Start the reader processes and return all in a list to the caller"""
    all_reader_procs = list()
    for ii in range(0, num_of_reader_procs):
        reader_p = Process(target=dynamicdist_reader, args=((qq),))
        reader_p.daemon = True
        reader_p.start()  # Launch reader_p() as another proc
        all_reader_procs.append(reader_p)
    return all_reader_procs


if __name__ == "__main__":
    num_dd_readers = 4
    qq = Queue()  # writer() writes to qq from _this_ process
    for num_dd_readers in range(2,8,2):
        for count in [10**4, 10**5, 10**6]:
            assert 0 < num_dd_readers < 32
            all_reader_procs = start_reader_procs(qq, num_dd_readers)
            dynamicdist_writer(numcalls=count, num_processors = len(all_reader_procs), qq=qq)  # Queue stuff to all reader_p()
            print("All reader processes are pulling numbers from the queue...")

            _start = time.time()
            for idx, a_reader_proc in enumerate(all_reader_procs):
                print(f"    Waiting for reader {idx}")
                a_reader_proc.join()  # Wait for a_reader_proc() to finish
                print(f"     Reader {idx} done")
            print(f"Sending {count} calls through Queue() with {num_dd_readers} listeners took {time.time()-_start} seconds")
