from typing import Dict
import numpy as np
import math

# # from timing import Timer 
# from time import perf_counter
# class Timer:
#    def __init__(self):
#       self._elapsed = 0
#       self._ht
#       self.start()

#    def start(self, name)
#    def start(self):
#       self._start = perf_counter()

#    def stop(self):
#       self._elapsed += perf_counter() - self._start()


class DynamicDist:

   def __init__(self, n_bins: int = 1000, buffer_size: int = 100000):
      # self.timer: Timer = Timer()
      self.reset(n_bins = n_bins, buffer_size = buffer_size)

   def reset(self, n_bins: int = 1000, buffer_size: int = 100000):
      # Size of the buffer used to hold the initial set of samples
      self.buffer_size: int = buffer_size
      # Number of bins
      self.n_bins: int = n_bins
      # Number of samples processed
      self.n: int = 0
      # Number of duplicate values
      self.n_dups: int = 0
      # Bin Size
      self.bin_size: np.double = np.nan
      # Dictionary to hold all the bins
      self.bins: Dict[np.double, int] = dict()
      # Bin offset
      self.bin_offset: np.double = np.nan

      # Initialize the buffer
      self._buffer: np.ndarray = np.empty((self.buffer_size), dtype = np.double)


   def compute_hist(self, data, freqs):
      # Performance Timer: Start
      # self.timer.start()

      # Map each data point to a bin
      bins = self.bin_offset + (np.floor((data-self.bin_offset)/self.bin_size)) * self.bin_size
      # Sort the bins (get the sorted indices)
      sorted_idx = bins.argsort()

      # Group the bins with the same value
      group_bins, group_start_idx, counts = np.unique(bins[sorted_idx], return_index = True, return_counts = True)
      # Sum the frequencies of the grouped bins
      group_freqs = np.add.reduceat(freqs[sorted_idx], group_start_idx)

      # Performance Timer: Stop
      # self.timer.stop()

      return group_bins, group_freqs


   def load_bins(self, redistribute: bool = False):
      # Performance Timer: Start
      # self.timer.start()

      # Check if the bin_size is nan
      if self.bin_size != self.bin_size:
         # Performance Timer: Start
         # self.timer.start("load_bins -> bin_size is nan")
         # Compute the bin size
         max_value = np.max(self._buffer[0: self.n])
         min_value = np.min(self._buffer[0: self.n])
         self.bin_offset = min_value
         self.bin_size = (max_value - min_value)/self.n_bins
         # Make sure the bin_size is not zero
         if self.bin_size < 1e-10:
            # Reset the bin_size
            self.bin_size = np.nan
            self.bin_offset = np.nan
            # All values are duplicates. Keep track of the number of duplicates
            if self.n_dups == 0:
               self.n_dups = self.n
            else:
               self.n_dups += self.n - 1
            # Reset the buffer, keep only the first item (if any)
            x = self._buffer[0]
            self._buffer = np.empty((self.buffer_size), dtype = np.double)
            if self.n:
               self._buffer[0] = x
               self.n = 1

            # Performance Timer: Stop
            # self.timer.stop("load_bins -> bin_size is nan")   
            # Exit
            return
         # Performance Timer: Stop
         # self.timer.stop("load_bins -> bin_size is nan")   

      if redistribute:
         # self.timer.start("load_bins: Dict --> Numpy Arrays")
         data = np.fromiter(self.bins.keys(), dtype = np.double, count = len(self.bins))
         freqs = np.fromiter(self.bins.values(), dtype = np.uint64, count = len(self.bins))

         # Compute the new bin size
         max_value = np.max(data)
         min_value = np.min(data)
         self.bin_offset = min_value
         bin_size = (max_value - min_value)/self.n_bins
         self.bin_size = np.ceil(bin_size/self.bin_size) * self.bin_size

         # self.timer.stop("load_bins: Dict --> Numpy Arrays")
      else:
         # Distribute the buffer
         data = self._buffer[0: self.n]
         freqs = np.ones((self.n), dtype = np.uint64)
         freqs[0] = max(1, self.n_dups)
         self.n_dups = 0

      # Group the bins
      group_bins, group_freqs = self.compute_hist(data, freqs)
      # Deallocate the buffer
      self._buffer = None

      # Load the bins and frequencies inside a dictionary
      # self.timer.start("load_bins: Numpy Arrays --> Dict")
      self.bins = dict(zip(group_bins, group_freqs))
      # self.timer.stop("load_bins: Numpy Arrays --> Dict")

      # Performance Timer: Stop
      # self.timer.stop()
      

   def add(self, x: np.double):
      # Performance Timer: Start
      # self.timer.start()

      # In case of NaNs (x != x is equivalent to np.isnan(x), but faster!), update the bin and exit
      if x != x:
         self.bins[np.nan] = self.bins.get(np.nan, 0) + 1
         # Performance Timer: Start
         # self.timer.stop()
         return
      
      # Check if we are past the initialization stage
      if self.n >= self.buffer_size:

         if len(self.bins) > 2*self.n_bins:
            # Reallocate the bins
            self.load_bins(redistribute = True)

         # Compute the center of the bin
         # key = (self.bin_offset + np.floor(x/self.bin_size)) * self.bin_size
         # self.timer.start("add -> compute key")
         key = self.bin_offset + (math.floor((x-self.bin_offset)/self.bin_size)) * self.bin_size
         # self.timer.stop("add -> compute key")
         # Add the value to the bin
         # self.timer.start("add -> update hash")
         self.bins[key] = self.bins.get(key, 0) + 1
         # self.timer.stop("add -> update hash")
         self.n += 1
      # Check if we are in the initialization stage
      else:
         # Add the value to the buffer
         # self.timer.start("add -> update buffer")
         self._buffer[self.n] = x
         # self.timer.stop("add -> update buffer")
         self.n += 1
         # Check if we have filled the buffer
         if self.n == self.buffer_size:
            # Load the self.bins dictionary
            self.load_bins()

      # Performance Timer: Stop
      # self.timer.stop()


   def histogram(self, n_bins = None):
      # Performance Timer: Start
      # self.timer.start()

      if n_bins:
         self.n_bins = n_bins
         
      self.load_bins(redistribute = self.bins)

      if self.n <= 1:
         # Special (degenerate) case, match whatever is produced by np.histogram
         hist, bins = np.histogram(self._buffer[0:self.n])
         hist *= max(1, self.n_dups)
      else:
         bins = np.fromiter(self.bins.keys(), dtype = np.double, count = len(self.bins))
         hist = np.fromiter(self.bins.values(), dtype = np.uint64, count = len(self.bins))

      # Performance Timer: Stop
      # self.timer.stop()

      return hist, bins

