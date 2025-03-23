import numpy as np
import math



class RocDist:
    def __init__(self, initialBins=10, initialSampleSize=10000, maxBins=5000, skipNans=True):
        self.initialHoldVector = np.empty((initialSampleSize), dtype=np.double)
        self.initialSampleSize = initialSampleSize
        self.initialBins = initialBins
        self.n = 0
        self.min = None
        self.max = None
        self.countBuckets = None
        self.binWidth = 0.0
        self.range = 0.0
        self.maxBins = maxBins 
        self.dups = 0
        self.dupVal = None
        self.nanSkipped = 0
        self.skipNans = skipNans
        self.nansSkipped = 0
        self.bins = None
        self.numBins = 0

    def whichBucket(self, f: np.double) -> int:
        index = int(self.numBins * ((f - self.min) / self.range)) 
        if index == self.numBins:
            index -= 1
        return index

    def buildInitialBucket(self):
        self.range = self.max - self.min # set up bins now that sample is full
        self.numBins = self.initialBins
        self.bins = np.zeros(self.numBins)
        for i in range(self.n): # this is not o(nlogn) but still o(n) slow 
            f = self.initialHoldVector[i]
            index = self.whichBucket(f)
            self.bins[index] += 1
            if self.dups > 0:
                f = self.dupVal
                index = self.whichBucket(f)
                self.bins[index] += self.dups
                self.dups = 0
        self.initialHoldVector = None # free temporary vector to hold initial values

    def add(self, f: np.double): # in the 'normal' case ( above sample size and within bins, make 0 method calls )
        if f != f: # comparison to missing returns false, same as if np.isnan(f)
            if self.skipNans:
                self.nansSkipped += 1
                return
            else:
                f = 0.
        if self.n < self.initialSampleSize: # still collecting data for bin placement
            self.initialHoldVector[self.n] = f
            if self.min == None or self.min > f:        
                self.min = f
            if self.max == None or self.max < f:
                self.max = f
            if self.n == self.initialSampleSize-1:
                if self.min == self.max: # defer setting up buckets until differing values received
                    self.dups += self.n
                    self.dupVal = f
                    self.n = 0
                else:
                    self.buildInitialBucket()
        else: # is a valid number, and already have bins
            if f > self.max: # add bins to the right
                binstoadd = math.ceil(self.numBins * ((f - self.min)/self.range)) - self.numBins
                newbins = np.zeros(binstoadd)
                self.bins = np.concatenate((self.bins,newbins), axis=None)
                self.numBins += binstoadd
                self.max = f
            if f < self.min: # add bins to the left
                binstoadd = math.ceil(self.numBins * ((self.max - f)/self.range)) - self.numBins
                newbins = np.zeros(binstoadd)
                self.bins = np.concatenate((newbins,self.bins), axis=None)
                self.numBins += binstoadd
                self.min = f
            index = self.whichBucket(f)
            self.bins[index] += 1
        self.n += 1

    def histogram(self):
        if self.n == 0:
            if self.nansSkipped:
                raise ValueError("autodetected range of [nan, nan] is not finite")
            if self.dups == 0:
                hist = np.zeros(10)
                bins = np.linspace(0, 1, 11)
                return hist, bins
            else:
                val = self.dupVal
                hist = np.concatenate([np.zeros(5),[self.dups],np.zeros(4)]).astype(int)
                bins = np.linspace(val-.5, val+.5,11)
                return hist, bins
        if self.n == 1:
            val = self.initialHoldVector[0]
            hist = np.concatenate((np.zeros(5),np.array([1]),np.zeros(4))).astype(int)
            bins = np.linspace(val-.5, val+.5,11)
            return hist, bins
        elif self.bins == None:
            if self.min == self.max:
                val = self.initialHoldVector[0]
                hist = np.concatenate([np.zeros(5),[self.n],np.zeros(4)]).astype(int)
                bins = np.linspace(val-.5, val+.5,11)
                return hist, bins
            else:
                self.buildInitialBucket()
                hist = self.bins
                bins = np.linspace(self.min, self.max, self.numBins+1)
                return hist, bins
        else:
            hist = self.bins
            bins = np.linspace(self.min, self.max, self.numBins+1)
            return hist, bins
