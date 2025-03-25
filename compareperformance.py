
import pytest
from rocdist import RocDist
import math
import numpy as np
from DynamicDist import DynamicDist
from FastDist import FastDist
from time import perf_counter

def test_sparse_multiple_groups(rd):
    sigma = 2
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        for v in vals:
            rd.add(v)
    for mu in range(4000,80000,1000):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        for v in vals:
            rd.add(v)
    hist, bins = rd.histogram()

if __name__ == "__main__":
    for rd in [FastDist(), DynamicDist()]:
        before = perf_counter()
        test_sparse_multiple_groups(rd)
        after = perf_counter()
        elapsed = after - before
        print(elapsed, rd)
