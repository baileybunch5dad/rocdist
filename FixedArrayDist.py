import numpy as np
import math
from typing import Tuple


# return the 100 quantiles regardless of input sample size
# in normalized linear time, with normalized o(1) add
class FixedArrayDist:
    def __init__(self, initialBins=100000, initialSampleSize=10000, skipNans=False):
        self._sample = None
        self._min = None
        self._max = None
        self._n = 0
        self._skipNans = skipNans
        self._initialSampleSize = initialSampleSize
        self._initialBins = initialBins
        self._bins = None
        self._nBins = 0
        self._range = 0
        self._nanCount = 0

    def rebin(self, 
              oldBins: np.array, 
              oldMin: np.double,
              oldMax: np.double,
              newMin: np.double, 
              newMax: np.double, 
              newNumBins: int) -> np.array: 
        oldNumBins = len(oldBins)
        newBins = np.zeros(newNumBins)
        oldRange = oldMax - oldMin
        if oldRange == 0:
            oldRange = 1
        oldBinWidth = oldRange / oldNumBins
        oldBinHalf = oldBinWidth / 2
        newRange = newMax - newMin
        newBins = np.zeros(newNumBins, dtype=int)
        for i in range(oldNumBins):
            value = oldMin + oldBinWidth * i + oldBinHalf
            count = oldBins[i]
            index = int(newNumBins * ((value - newMin) / newRange)) 
            if index == newNumBins: # last interval is closed
                index -= 1
            newBins[index] += count
        return newBins

    # for trivial/tiny cases, use numpy hist, for large build quantiles dynamically
    def histogram(self) -> Tuple[np.array, np.array]: 
        if self._n == 0:
            return np.histogram(np.empty(0))
        if self._n <= self._initialSampleSize:
            return np.histogram(self._sample[0:self._n], bins=100)
        hist = self.rebin(self._bins, self._min, self._max, self._min, self._max, 100)
        bins = np.linspace(self._min, self._max, 101)
        return hist, bins
    
    def add(self, x):
        if (x != x):
            if self._skipNans:
                self._nanCount += 1
                x = 0
            else:
                raise ValueError("add(nan) with skipsNans=False")
        if self._n >= self._initialSampleSize: # put case initsample..inf first for speed
            if x < self._min:
                self._bins = self.rebin(self._bins, self._min, self._max, x, self._max, self._nBins)
                self._min = x
                self._range = self._max - self._min
            if x > self._max:
                self._bins = self.rebin(self._bins, self._min, self._max, self._min, x, self._nBins)
                self._max = x
                self._range = self._max - self._min
            index = int(self._nBins * ((x - self._min) / self._range)) 
            if index == self._nBins: # last interval is closed
                index -= 1
            self._bins[index] += 1
        elif self._n == 0:
            self._sample = np.empty(self._initialBins, dtype=type(x))
            self._sample[0] = x
        elif self._n < self._initialSampleSize-1:
            self._sample[self._n] = x
        else: #adding last elt to sample, convert initial tiny sample to bins using np hist
            self._sample[self._n] = x
            hist, bins = np.histogram(self._sample, bins=self._initialBins)
            self._min = bins[0]
            self._max = bins[-1]
            self._range = self._max - self._min
            self._bins = hist
            self._nBins = len(self._bins)
        self._n += 1

