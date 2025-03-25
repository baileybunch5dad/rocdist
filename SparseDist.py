import numpy as np
import math

class SparseDist:
    def __init__(self, sampleSize=100000, initialBins = 100000, skipNans=True):
        self._sampleSize = sampleSize
        self._numSamples = 0
        self._sample = np.empty((sampleSize), dtype=np.double)
        self._numBins = 0
        self._min = None
        self._max = None
        self._binWidth = 0.0
        self._range = 0.0
        self._nanSkipped = 0
        self._skipNans = skipNans
        self._bins = None
        self._numBins = 0
        self._ht = None
        self._usingHash = False
        self._n = 0
        self._initialBins = initialBins
        self._expansions = 0

    def add(self, f: np.double): # in the 'normal' case ( above sample size and within bins, make 0 method calls )
        if f != f: # comparison to missing returns false, same as if np.isnan(f)
            if self.skipNans:
                self.nansSkipped += 1
                return
            else:
                f = 0.
        if self._n >= self._sampleSize:
            if f > self._max: # need growth to the right 
                self._expansions += 1
                if not self._usingHash: # convert array to hash
                    self._ht = {}
                    for i in range(self._numBins): # after this, ht is populated with prior values
                        self._ht[i] = self._bins[i]
                    self._usingHash = True
                binstoadd = math.ceil((f - self._max)/ self._binWidth)
                self._numBins += binstoadd
                self._ht[self._numBins-1] = 1 # new rightmost key
                self._max = f  # binwidth does not change, but limits, range and numbins does
                self._range = self._max - self._min
            elif f < self._min:
                self._expansions += 1
                binstoadd = math.ceil((self.min-f)/self.binWidth)
                if not self._usingHash: # convert array to hash first time
                    self._ht = {}
                    for i in range(self._numBins): # after this, ht is populated with prior values
                        self._ht[i] = self._bins[i]
                    self._usingHash = True
                # guaranteed to be using hash here
                # on any left adds, increment key in bins to the right
                binstoadd = math.ceil((f - self._max)/ self._binWidth)
                newht = {}
                for k,v in self._ht.items():
                    newht[k+binstoadd] = v
                self._ht = newht
                self._numBins += binstoadd
                self._ht[0] = 1 # new leftmost key
                self._min = f
                self._range = self._max - self._min
            else: # within max, min range, use relative position to get ht key
                index = int(self._numBins * ((f - self._min) / self._range)) 
                if index == self._numBins:
                    index -= 1
                if self._usingHash:
                    self._ht[index] = self._ht.get(index,0) + 1
                else:
                    self._bins[index] += 1
        elif self._n < self._sampleSize-1:
            self._sample[self._n] = f
        else: #adding last elt to sample, convert initial tiny sample to bins using np hist
            self._sample[self._n] = f
            hist, bins = np.histogram(self._sample, bins=self._initialBins)
            self._min = bins[0]
            self._max = bins[-1]
            self._range = self._max - self._min
            self._bins = hist
            self._numBins = self._initialBins
            self._binWidth = self._range / self._initialBins
        self._n += 1

    def histogram(self):
        if self._n == 0:
            return np.histogram(np.empty(0), bins=100)
        elif self._n <= self._sampleSize:
            return np.histogram(self._sample[0:self._n], bins=100)
        halfbin = self._binWidth/2
        if not self._usingHash: # everything fit in the initial bins
            midpoints = np.empty((self._numBins))
            counts = np.zeros((self._numBins), dtype=int)
            for i in range(self._numBins):
                midpoints[i] = self._min + self._binWidth*i + halfbin
            return np.histogram(midpoints, weights=counts, bins=100)
        else:
            n = len(self._ht)
            midpoints = np.empty((n))
            counts = np.zeros((n), dtype=int)
            i = 0
            for key,val in self._ht.items():
                midpoints[i] = self._min + self._binWidth*key + halfbin
                counts[i] = val
                i += 1
            return np.histogram(midpoints, weights=counts, bins=100)
