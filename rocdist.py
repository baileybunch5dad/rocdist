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
        self.ht = None
        self.usingSparse = False

    def sigdigit(self, x, p=4): # round x to p digits so 'midpoints' are calculated consistently
        x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
        mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
        return np.round(x * mags) / mags

    def whichBucket(self, f: np.double) -> int:
        index = int(self.numBins * ((f - self.min) / self.range)) 
        if index == self.numBins:
            index -= 1
        return index
    
    def midpoint(self, index):
        key = self.min + index * self.binWidth + self.binWidth/2
        key = self.sigdigit(key)
        return key
    
    def makesparse(self):
        self.ht = {}
        half = self.binWidth / 2
        for index in range(self.numBins):
            count = self.bins[index]
            key = self.midpoint(index)
            self.ht[key] = count
        self.usingSparse = True
        self.bins = None

    def buildInitialBucket(self):
        self.range = self.max - self.min # set up bins now that sample is full
        self.numBins = self.initialBins
        self.binWidth = self.range / self.numBins
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
                binstoadd = math.ceil((f - self.max)/ self.binWidth)
                if (not self.usingSparse) and (binstoadd + self.numBins > self.maxBins):
                    self.makesparse()
                # self.makesparse changes self.usingsparse flag, so need to query again
                if not self.usingSparse: # dense case, grow vec
                    newbins = np.zeros(binstoadd)
                    self.bins = np.concatenate((self.bins,newbins), axis=None) # add to right
                self.numBins += binstoadd
                self.max += binstoadd * self.binWidth
                self.range = self.max - self.min
            if f < self.min: # add bins to the left
                binstoadd = math.ceil((self.min-f)/self.binWidth)
                if (not self.usingSparse) and (binstoadd + self.numBins > self.maxBins):
                    self.makesparse()
                # self.makesparse changes self.usingsparse flag, so need to query again
                if not self.usingSparse: # dense case, grow vec
                    newbins = np.zeros(binstoadd)
                    self.bins = np.concatenate((newbins,self.bins), axis=None) # add to left
                self.numBins += binstoadd
                self.min -= binstoadd * self.binWidth
                self.range = self.max - self.min
            index = self.whichBucket(f)
            if self.usingSparse:
                key = self.midpoint(index)
                self.ht.setdefault(key, 0)
                self.ht[key] += 1
            else:
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
        if not isinstance(self.bins, np.ndarray):
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
        
    def sparsehist(self): # return midpoints and counts as two sorted vectors
        n = self.numBins
        midpoints = np.empty((n))
        counts = np.empty((n))
        if not self.usingSparse:
            for i in range(self.numBins):
                midpoints[i] = self.midpoint(i)
                counts[i] = self.bins[i]
        else:
            sorted_items = sorted(self.ht.items())
            i = 0
            for key, value in sorted_items:
                midpoints[i] = key
                counts[i] = value
                i += 1
        return midpoints, counts



