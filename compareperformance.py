
from SparseDist import SparseDist
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FixedArrayDist
from time import perf_counter
import cProfile

cumsum = {}

def compare_to_numpy(rd, bigarray: np.array):
    global cumsum
    before = perf_counter()
    for v in bigarray:
        rd.add(v)
    if isinstance(rd, DynamicDist):
        hist, bins = rd.histogram(n_bins = 100)
        n_bins = int(np.ceil((np.max(bigarray) - np.min(bigarray))/rd.bin_size))
    else:
        hist, bins = rd.histogram()
        n_bins = 100        
    after = perf_counter()
    elapsed = after - before
    algorithm = type(rd).__name__
    print(elapsed, type(rd).__name__)
    cumsum[algorithm] = cumsum.get(algorithm,0) + elapsed
    nhist, nbins = np.histogram(bigarray, bins=n_bins)
    return hist, bins, nhist, nbins
    
def test_random_uniform(rd):
    vals = np.random.uniform(low=0, high=100, size=100000000)
    return compare_to_numpy(rd, vals)

def test_random_uniform_monotonic(rd):
    vals = np.random.uniform(low=0, high=100, size=100000000)
    vals = np.sort(vals)
    return compare_to_numpy(rd, vals)

def test_sparse_multiple_groups(rd):
    sigma = 5
    bigarray = np.empty((0))
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    sigma = 700
    for mu in range(4000,80000,1000): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    return compare_to_numpy(rd, bigarray)


def Main():
    for i in range(3):
        for whichTest in [test_random_uniform, test_random_uniform_monotonic, test_sparse_multiple_groups]:
            print(whichTest.__name__)
            for rd in [DynamicDist(), SparseDist()]: # FixedDist()
                hist, bins, nhist, nbins = whichTest(rd)


if __name__ == "__main__":
    # cProfile.run('Main()')
    Main()
    print('Cumulative Time',cumsum)
