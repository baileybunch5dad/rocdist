
from SparseDist import SparseDist
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FixedArrayDist
from time import perf_counter

def test_sparse_multiple_groups(rd):
    sigma = 5
    bigarray = np.empty((0))
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
        for v in vals:
            rd.add(v)
    sigma = 700
    for mu in range(4000,80000,1000): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
        for v in vals:
            rd.add(v)
    hist, bins = rd.histogram()
    nhist, nbins = np.histogram(bigarray, bins=100)
    return hist, bins, nhist, nbins

if __name__ == "__main__":
    for rd in [DynamicDist(), SparseDist()]: # FixedDist()
        before = perf_counter()
        hist, bins, nhist, nbins = test_sparse_multiple_groups(rd)
        after = perf_counter()
        elapsed = after - before
        print(elapsed, type(rd).__name__)
        print(hist.sum(), hist)
        print(nhist.sum(), nhist)
