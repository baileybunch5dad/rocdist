import numpy as np
import sys

class SparseDist:
    def __init__(self, sampleSize=10000, initialBins = 1000, skipNans=True):
        self.sampleSize : int = sampleSize
        self.n : int = 0
        self.min : np.double = sys.float_info.max
        self.max : np.double = -sys.float_info.max
        self.binWidth : np.double = 0.0
        self.nans : int = 0
        self.skipNans : bool = skipNans
        self.initialBins = initialBins
        self.bins = np.empty((sampleSize), dtype=np.double) # switches from array to hash 
        self.finishedWithSample = False

    def midpointcounthist(self, bins : int = 1000):
        midpoints = self.bins.keys() 
        midpoints = np.array(list(midpoints)).astype(float) + self.min + self.binWidth/2
        counts = np.array(list(self.bins.values()))
        return np.histogram(midpoints, weights=counts, bins=bins)
    
    def add(self, x: np.double): # in the 'normal' case ( above sample size and within bins, make 0 method calls )
        if x != x: # comparison to missing returns false, same as if np.isnan(f)
            self.nans += 1
            return
        if self.n >= self.sampleSize:
            key = int((x - self.min) // self.binWidth) # // python floor operator
            curval = self.bins.get(key,0)
            if curval == 0:
                self.bins[key] = 1
                if len(self.bins) > 2 * self.initialBins: # rebalance
                    hist, bins = self.midpointcounthist(bins=self.initialBins)
                    self.min, self.binWidth = bins[0], bins[1] - bins[0]
                    self.bins = {k:v for k,v in enumerate(hist) if v > 0}
            else:
                self.bins[key] = curval + 1
        else:
            self.bins[self.n] = x
            if self.n == self.sampleSize - 1: # just filled in last slot, convert
                hist, bins = np.histogram(self.bins, bins=self.initialBins)
                self.min, self.binWidth = bins[0], bins[1] - bins[0]
                self.bins = {k:v for k,v in enumerate(hist) if v > 0}
        self.n += 1
                     
    def histogram(self, maxBins=100):
        if self.n == 0:
            return np.histogram(np.empty(0), bins=maxBins)
        if self.n < self.sampleSize:
            return np.histogram(self.bins[0:self.n], bins=maxBins)
        return self.midpointcounthist(bins=maxBins)
