import numpy as np
from time import perf_counter

N = 1_000_000
total_time_array = 0
total_time_hash = 0
n_bins = 1000
 
bins_array = np.zeros((n_bins), dtype = np.uint64)
bins_hash = dict()
for i in range(N):
   x = np.random.randint(0, n_bins * 999)
   key = x/1000.0 # Make the key a float, should be a worst case for the hash
   intkey = int(key)
   start = perf_counter()
   bins_array[intkey] += 1
   end = perf_counter()
   elapsed = end - start
   total_time_array += elapsed
 
   start = perf_counter()
   bins_hash[intkey] = bins_hash.get(key, 0) + 1
   end = perf_counter()
   elapsed = end - start
   total_time_hash += elapsed
 
average_time_array = total_time_array/N
average_time_hash = total_time_hash/N
 
print(f"{total_time_array=}   {average_time_array=}")
print(f"{total_time_hash=}   {average_time_hash=}")
 
 
 
 