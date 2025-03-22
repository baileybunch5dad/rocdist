import numpy as np

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

class RocDist:
    def __init__(self, initialBins=100, initialSampleSize=1000, maxBins=5000, skipNans=True):
        self.initialHoldvector = np.array(initialSampleSize, dtype=np.double)
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
        self.nanSkipped = 0
        self.skipNans = skipNans

    def add(self, f: np.double):
        if f != f:
            if self.skipNans:
                nansSkipped += 1
                return
            else:
                f = 0.
        if self.n < self.initialSampleSize:
            self.initialHoldVector[self.n] = f
            if self.min == None or self.min > f:        
                self.min = f
            if self.max == None or self.max < f:
                self.max = f
        elif self.n == self.initialSampleSize:
            self.range = self.max - self.min
            self.binWidth = (self.max - self.min) / self.initialBins




