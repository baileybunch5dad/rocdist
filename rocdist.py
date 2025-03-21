import numpy as np

# RocDist
# Low Memory
# Zero Sort
# Fast Histogram builder


class RocDist:
    def __init__(self, initialBins=100, initialSampleSize=1000):
        self.initialHoldvector = np.array(initialSampleSize, dtype=np.double)
        self.initialSampleSize = initialSampleSize
        self.initialBins = initialBins
        self.n = 0
        self.min = None
        self.max = None
        self.countBuckets = None
        self.binWidth = 0.0
        self.range = 0.0

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




