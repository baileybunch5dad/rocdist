import time
import multiprocessing as mp
import sys
import os

def do_something():
    print(f'{os.getpid()=} {sys.executable=} {sys.argv=}')
    print('Sleeping 10 seconds...')
    time.sleep(10)
    print('Done Sleeping...')
    
def benchmark():
    # sys.argv = [r'myfile.py']
    # mp.set_executable(r'C:\path_to_Python_install\python.exe')

    start = time.perf_counter()

    p1 = mp.Process(target=do_something)
    p2 = mp.Process(target=do_something)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start,2)} second(s)')
 
if __name__ == '__main__':
    benchmark()

