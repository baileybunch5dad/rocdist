import numpy as np
import sys
from typing import Dict

class SparseDist:
    def __init__(self, n_bins: int = 1000, buffer_size: int = 100000, timer_enabled: bool = False):
        self.reset(n_bins = n_bins, buffer_size = buffer_size)

    def reset(self, n_bins: int = 1000, buffer_size: int = 100000):
        # Size of the buffer used to hold the initial set of samples
        self.buffer_size: int = buffer_size
        # Number of bins
        self.n_bins: int = n_bins
        # Number of samples processed
        self.n: int = 0
        # Bin Size
        self.bin_size: np.double = np.nan
        # Dictionary to hold all the bins
        self.bins: Dict[np.double, int] = dict()
        # Bin offset
        self.bin_offset: np.double = np.nan
        # upper and lower values seen in the data
        self.min : np.double = sys.float_info.max
        self.max : np.double = -sys.float_info.max
        # how many NaNs (Not a Number) have been encountered
        self.nans: int = 0 
        # Initialize the buffer
        self._buffer: list = [None] * self.buffer_size #np.empty((self.buffer_size), dtype = np.double)

    def nphist(self, buckets):
        values = np.array(list(self.bins.keys())).astype(float) * self.bin_size + self.bin_offset
        # values += self.bin_size/2
        counts = np.array(list(self.bins.values()))
        hist, bins = np.histogram(values, weights=counts, bins=buckets)
        self.min, self.bin_size, self.max = bins[0], bins[1] - bins[0], bins[-1]
        self.bin_offset = self.min
        self.bins = {k:v for k,v in enumerate(hist) if v > 0}
        return hist, bins

    
    def add(self, x: np.double): # in the 'normal' case ( above sample size and within bins, make 0 method calls )
        if x != x: # comparison to missing returns false, same as if np.isnan(f)
            self.nans += 1
            return
        if self.n >= self.buffer_size:
            key = int((x - self.bin_offset) // self.bin_size) # // python floor operator
            curval = self.bins.get(key,0)
            if curval == 0:
                # not only need to check min max on new bucket
                self.bins[key] = 1
                if x > self.max:
                    self.max = x
                if x < self.min:
                    self.min = x
                if len(self.bins) > 2 * self.n_bins: # rebalance
                    buckets = np.linspace(self.min, self.max, self.n_bins+1) # match np exactly
                    self.nphist(buckets = buckets)
            else:
                self.bins[key] = curval + 1
        else:
            self._buffer[self.n] = x
            if self.n == self.buffer_size - 1: # just filled in last slot, convert
                hist, bins = np.histogram(self._buffer, bins=self.n_bins)
                self._buffer = None # free memory
                self.min, self.bin_size, self.max = bins[0], bins[1] - bins[0], bins[-1]
                self.bin_offset = self.min
                self.bins = {k:v for k,v in enumerate(hist) if v > 0}
        self.n += 1
                     
    def histogram(self, n_bins=100):
        if self.n == 0:
            return np.histogram(np.empty(0), bins=n_bins)
        if self.n < self.buffer_size:
            return np.histogram(self._buffer[0:self.n], bins=n_bins)
        return self.nphist(buckets=n_bins)
