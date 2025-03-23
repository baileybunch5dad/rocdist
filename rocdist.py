import numpy as np
import math

# RocDist
# Low Memory
# Zero Sort
# Fast Histogram builder
#
# Author: Rocco Cannizzaro
# Typist: Chris
#
# the algorithm has as its basic requirement to be faster and use much less memory
# than numpy.histogram, which requires all values in memory and then to be sorted
# 
# Algorithm
# collect a few samples, make bins based on them with counts at a small threshold
# o(1) insertion during initial phase, add same width bins as needed
#
# on insertion of a new element, just increment the count in the appropriate bucket if it fit, o(1)
# if it does not fit, allocate new bucket of previous width to that and, and dup into new structure, o(n)
#
# if has "normalized" distribution, algorithm will be o(n) rather than o(nlogn) of numpy histogram
# and at the same time, use only a single array of size nbuckets, so extremely low memory
#
# pathological case detection
# if the number of buckets would grow by an exorbitant amount,
# for example if the input contained a repeated value setting the bucket width to zero,
# or similarly some tightly clustered values, then got values "relatively" far away 
# (based on number of bins it would have to create of that identical size)
# throw an error if growth amount greater than some threshold (alternatively rescale the existing buckets) 
# for example, if there were millions of random numbers between 0 and 1,
# and a hundred buckets were made to hold the counts of numbers 0.00<=x<0.001, 0.01<=x<0.02
# then another number comes in like 1e15 that with the original binWidth of 0.01 would cause an explosion
# return the exception
#
# next pathological case is all value are identical
#
# next pathological case is identical valuers initially (binwidth=0) in initial sample size
# followed by differing values
# detect this condition by range detection on initial sample
# 
# next pathological case is different distributions in data, for example two normal 
# distribution with different center and scale that the intial is received prior to the latter
# similar handling to pathological clustering
#
# note, following numpy.histogram
# All but the last (righthand-most) bin is half-open. In other words, if bins is:
class RocDist:
    def __init__(self, initialBins=100, initialSampleSize=10000, maxBins=5000, skipNans=True):
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

if __name__ == "__main__":
    mu, sigma = 100.0, 10.0 # mean and standard deviation
    manyvalues = np.random.normal(loc=mu, scale=sigma, size=1000000)
    print(manyvalues)
    rd = RocDist()
    for m in manyvalues:
        rd.add(m)




