import numpy as np

# RocDist
# Low Memory
# Zero Sort
# Fast Histogram builder
#
# Author: Rocco Cannizzaro
# Typist: Chris
#
# Algorithm
# collect a few samples, make bins based on them with counts at a small threshold
# o(1) insertion during initial phase
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
# throw an error if growth amount greater than MaxGrowthPercentage
# for example, if there were millions of random numbers between 0 and 1,
# and a hundred buckets were made to hold the counts of numbers 0.00<=x<0.001, 0.01<=x<0.02
# then another number comes in like 1e15 that with the original binWidth of 0.01 would cause an explosion
# return the exception
#
# other than this one case, the algorithm has as its basic requirement to be faster and use much less memory
# than numpy.histogram, which requires all values
# 

class RocDist:
    def __init__(self, initialBins=100, initialSampleSize=1000, maxGrowthPercentage=200):
        self.initialHoldvector = np.array(initialSampleSize, dtype=np.double)
        self.initialSampleSize = initialSampleSize
        self.initialBins = initialBins
        self.n = 0
        self.min = None
        self.max = None
        self.countBuckets = None
        self.binWidth = 0.0
        self.range = 0.0
        self.maxPathologicalGrowthPercentage = maxPathologicalGrowthPercentage

    def add(self, f: np.double):
        if self.n < self.initialSampleSize:
            self.initialHoldVector[self.n] = f
            if self.min == None or self.min > f:        
                self.min = f
            if self.max == None or self.max < f:
                self.max = f
        elif self.n == self.initialSampleSize:
            self.range = self.max - self.min
            self.binWidth = (self.max - self.min) / self.initialBins




