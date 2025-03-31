
from SparseDist import SparseDist
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FixedArrayDist
from time import perf_counter
import cProfile
import matplotlib.pyplot as plt

cumsum = {}

def compare_to_numpy(rd, bigarray: np.array):
    global cumsum
    before = perf_counter()
    for v in bigarray:
        rd.add(v)
    if isinstance(rd, DynamicDist):
        hist, bins = rd.histogram(n_bins = 100)
        # make hist and binse 'dense'
        n_bins = 100
        newBins = np.linspace(rd.bin_offset, rd.bin_offset + rd.bin_size * (n_bins+1), n_bins+1)
        newHist = np.array([rd.bins.get(key, 0) for key in range(n_bins)])
        hist, bins = newHist, newBins
        # n_bins = int(np.ceil((np.max(bigarray) - np.min(bigarray))/rd.bin_size))

    else:
        hist, bins = rd.histogram()
        n_bins = 100        
    after = perf_counter()
    elapsed = after - before
    algorithm = type(rd).__name__
    cumsum[algorithm] = cumsum.get(algorithm,0) + elapsed
    nhist, nbins = np.histogram(bigarray, bins=n_bins)
    histerrors = sum([abs(x-y) for x,y in zip(hist, nhist)])
    print(elapsed, histerrors, histerrors/hist.sum(), type(rd).__name__)
    plt.stairs(hist, bins, label=algorithm)
    plt.stairs(nhist, nbins, label='numpy')
    plt.legend()
    plt.show()
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
    for mu in range(4000,40000,200): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    return compare_to_numpy(rd, bigarray)


def Main():
    sigma = 5
    bigarray = np.empty((0))
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    sigma = 300
    for mu in range(4000,40000,2000): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    dd = DynamicDist()
    sd = SparseDist()
    for v in bigarray:
        dd.add(v)
        sd.add(v)
    ddhist, ddbins = dd.histogram(n_bins = 100)
    n_bins = 100
    ddbins = np.linspace(dd.bin_offset, dd.bin_offset + dd.bin_size * (n_bins+1), n_bins+1)
    ddhist = np.array([dd.bins.get(key, 0) for key in range(n_bins)])
    sdhist, sdbins = sd.histogram()
    nphist, npbins = np.histogram(bigarray, bins=n_bins)
    plt.stairs(ddhist, ddbins, label='DynamicDist')
    plt.stairs(sdhist, sdbins, label='SparseDist')
    plt.stairs(nphist, npbins, label='numpy')
    plt.legend()
    plt.show()


def Main2():
    for i in range(3):
        for whichTest in [test_random_uniform, test_random_uniform_monotonic, test_sparse_multiple_groups]:
            print(whichTest.__name__)
            for rd in [DynamicDist(), SparseDist()]: # FixedDist()
                hist, bins, nhist, nbins = whichTest(rd)


if __name__ == "__main__":
    # cProfile.run('Main()')
    Main()
    # print('Cumulative Time',cumsum)
