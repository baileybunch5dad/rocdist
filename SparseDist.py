import numpy as np
import math
from enum import Enum
from typing import Dict

class State(Enum):
    COLLECTING_SAMPLES = 1
    HIST_ARRAY = 2
    HASHTABLE = 3

class SparseDist:
    def __init__(self, sampleSize=10000, initialBins = 1000, skipNans=True):
        self._sampleSize = sampleSize
        self._n : int = 0
        self._min : np.double = None
        self._binWidth : np.double = 0.0
        self._nansSkipped : int = 0
        self._skipNans : bool = skipNans
        self._initialBins = initialBins
        self._bins = np.empty((sampleSize), dtype=np.double) 

    def add(self, f: np.double): # in the 'normal' case ( above sample size and within bins, make 0 method calls )
        if f != f: # comparison to missing returns false, same as if np.isnan(f)
            if self.skipNans:
                self.nansSkipped += 1
                return
            else:
                f = 0.
        if self._n >= self._sampleSize:
            index = int((f - self._min) // self._binWidth) # // is python floor operator, allow negative keys, //-3.2 is -4.0
            # if index == self._numBins: # end interval is open, priors are closed
            #     index -= 1            
            self._bins[index] = self._bins.get(index,0) + 1     
            if len(self._bins) > 4*self._initialBins: # rebalance
                hist, bins = self.histogram(maxBins=self._initialBins)
                self._min, self._binWidth = bins[0], bins[1] - bins[0]
                self._bins = {k:v for k,v in enumerate(hist) if v > 0}
        else:
            self._bins[self._n] = f
            if self._n == self._sampleSize - 1: # just filled in last slot, convert
                hist, bins = np.histogram(self._bins, bins=self._initialBins)
                self._min, self._binWidth = bins[0], bins[1] - bins[0]
                self._bins = {k:v for k,v in enumerate(hist) if v > 0}
        self._n += 1
                     
    def histogram(self, maxBins=100):
        if self._n == 0:
            return np.histogram(np.empty(0), bins=maxBins)
        if self._n < self._sampleSize:
            return np.histogram(self._bins[0:self._n], bins=maxBins)
        n = len(self._bins)
        midpoints = np.empty((n))
        counts = np.zeros((n), dtype=int)
        i = 0
        for key,val in self._bins.items():
            midpoints[i] = self._min + self._binWidth*key + self._binWidth/2
            counts[i] = val
            i += 1
        return np.histogram(midpoints, weights=counts, bins=maxBins)
