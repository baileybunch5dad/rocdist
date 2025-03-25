from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from typing import Dict
import numpy as np

class DynamicDist(BaseModel):
   model_config = ConfigDict(arbitrary_types_allowed = True)

   # Size of the buffer used to hold the initial set of samples
   buffer_size: int = 10000
   # Number of bins
   n_bins: int = 1000
   # Number of samples processed
   n: int = 0
   # Number of duplicate values
   n_dups: int = 0
   # Bin Size
   bin_size: np.double = np.nan
   # Dictionary to hold all the bins
   bins: Dict[np.double, int] = Field(default_factory = dict)
   # Bin offset (in the range [0, 1])
   bin_offset: np.double = np.nan

   # Private attribute for the buffer
   _buffer: np.ndarray = PrivateAttr()

   # Post Init: initialize the buffer
   def model_post_init(self, __context):
      self._buffer = np.empty((self.buffer_size), dtype = np.double)


   def compute_hist(self, data, freqs):
      # Map each data point to a bin
      bins = self.bin_offset + (np.floor((data-self.bin_offset)/self.bin_size)) * self.bin_size
      # Sort the bins (get the sorted indices)
      sorted_idx = bins.argsort()

      # Group the bins with the same value
      group_bins, group_start_idx, counts = np.unique(bins[sorted_idx], return_index = True, return_counts = True)
      # Sum the frequencies of the grouped bins
      group_freqs = np.add.reduceat(freqs[sorted_idx], group_start_idx)

      return group_bins, group_freqs


   def load_bins(self, redistribute: bool = False):

      if np.isnan(self.bin_size):
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
            # Exit
            return

      if redistribute:
         # Redistribute existing bins
         data = np.array(list(self.bins.keys()), dtype = np.double)
         freqs = np.array(list(self.bins.values()), dtype = np.double)
      else:
         # Distribute the buffer
         data = self._buffer[0: self.n]
         freqs = np.ones((self.n), dtype = np.double)
         freqs[0] = max(1, self.n_dups)
         self.n_dups = 0

      # Group the bins
      group_bins, group_freqs = self.compute_hist(data, freqs)
      # Deallocate the buffer
      self._buffer = None

      # Load the bins and frequencies inside a dictionary
      self.bins = dict(zip(group_bins, group_freqs))
      

   def add(self, x: np.double):
      # In case of NaNs, update the bin and exit
      if np.isnan(x):
         self.bins[np.nan] = self.bins.get(np.nan, 0) + 1
         return
      
      # Check if we are past the initialization stage
      if self.n >= self.buffer_size:

         if len(self.bins) > 2*self.n_bins:
            # Double the bin size
            self.bin_size = self.bin_size * 2
            # Reallocate the bins
            self.load_bins(redistribute = True)

         # Compute the center of the bin
         # key = (self.bin_offset + np.floor(x/self.bin_size)) * self.bin_size
         key = self.bin_offset + (np.floor((x-self.bin_offset)/self.bin_size)) * self.bin_size
         # Add the value to the bin
         self.bins[key] = self.bins.get(key, 0) + 1
         self.n += 1
      # Check if we are in the initialization stage
      else:
         # Add the value to the buffer
         self._buffer[self.n] = x
         self.n += 1
         # Check if we have filled the buffer
         if self.n == self.buffer_size:
            # Load the self.bins dictionary
            self.load_bins()

   def histogram(self):
      if not self.bins:
         # Make sure the bins dictionary is initialized
         self.load_bins()

      if self.n <= 1:
         # Special (degenerate) case, match whatever is produced by np.histogram
         hist, bins = np.histogram(self._buffer[0:self.n])
         hist *= max(1, self.n_dups)
      else:
         bins = np.array(list(self.bins.keys()), dtype = np.double)
         hist = np.array(list(self.bins.values()), dtype = np.double)

      return hist, bins

