from SparseDist import SparseDist
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FixedArrayDist
from time import perf_counter
import cProfile
import matplotlib.pyplot as plt
import inspect


#
# Compute root mean square error 
# based on distance from the upper left histogram corners
# where the values are x=binstart, y=count
#
# and the algorithm (DynamicDist, SparseDist) computes 'predicted'
# with numpy on all data computal 'actual'
#
def getRMSE(predHist : np.array, predBins : np.array, actHist : np.array, actBins : np.array):
    predicted = np.transpose([predHist,predBins[:-1]])
    actual = np.transpose([actHist,actBins[:-1]])
    distances = np.sqrt(np.sum((predicted - actual)**2, axis=1))
    # now we have all the distances, square them, sum them, didivde by n, and sqrt is rmse
    squareerror = np.square(distances)
    meansquareerror = squareerror.sum() / len(distances)
    rmse = np.sqrt(meansquareerror)
    return rmse

#
# Convert DynamicDist sparse bins and counts to match numpy dense bins and counts
# 
# e.g. asking for 100 bins in DynamicDist returns up to 100 bins, but possibly fewer
#
# DynamicDist internally after hisogram call in its sparse hashtable may have negative keys
# and its bin_offset is not a "minimum" ( because of the keys )
#
# Multiple way to patch, one is get the true min, add offset, recompute keys in loop
# Simplest is to use bins as data, and counts as weights, and call numpy histogram
def convertDynamicDistToNumpy(dd, n_bins=100):
    ddhist, ddbins = dd.histogram(n_bins = n_bins)
    ddminval = ddbins[0]
    ddbinsize = dd.bin_size
    ddmaxval = ddbins[-1] + ddbinsize
    newbins = np.linspace(ddminval, ddmaxval, n_bins+1)
    midpoints = ddbins + ddbinsize/2
    ddhist, ddbins = np.histogram(midpoints, weights=ddhist, bins=newbins)
    return ddhist, ddbins
 
#
# Overlay the hisogram of the predictor versus the actual
#
def graphit(testname: str, name: str, elapsed: float, rmse: float,
            predhist: np.array, predbins: np.array,
            acthist: np.array, actbins: np.array):
    plt.stairs(acthist, actbins, label='numpy')
    plt.stairs(predhist, predbins, label=name)
    plt.legend()
    plt.title(f'{testname} {name} Time={elapsed:.2f} RMSE={rmse:.2f}')
    plt.show()
     
#
# Compare an algorithm that does not hold the entire data and must 'estimate'
# an a given data set by refining a sample to something that hold the entire data
#    
def compare_to_numpy(bigarray: np.array):
    testname = inspect.stack()[1].function
    actualhist, actualbins = np.histogram(bigarray, bins=100)
    for algorithm in [DynamicDist(), SparseDist()]:
        name = type(algorithm).__name__
        before = perf_counter()
        for v in bigarray: 
            algorithm.add(v)
        if isinstance(algorithm,DynamicDist):
            predhist, predbins = convertDynamicDistToNumpy(algorithm, n_bins=100)
        else:
            predhist, predbins = algorithm.histogram()
        # print(f'{actualhist.sum()=} {predhist.sum()=}')
        elapsed = perf_counter() - before
        rmse = getRMSE(predhist, predbins, actualhist, actualbins)
        print(f'{testname} {name} Time={elapsed:.2f} RMSE={rmse:.2f}')
        graphit(testname,name,elapsed,rmse,predhist, predbins, actualhist, actualbins)

def test_random_uniform():
    vals = np.random.uniform(low=0, high=100, size=100000000)
    return compare_to_numpy(vals)

def test_random_uniform_monotonic():
    vals = np.random.uniform(low=0, high=100, size=100000000)
    vals = np.sort(vals)
    return compare_to_numpy(vals)

def test_sparse_multiple_groups():
    sigma = 5
    bigarray = np.empty((0))
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    sigma = 700
    for mu in range(4000,40000,200): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    return compare_to_numpy(bigarray)

def Main():
    for i in range(3):
        for whichTest in [test_random_uniform, test_random_uniform_monotonic, test_sparse_multiple_groups]:
            print(whichTest.__name__)
            whichTest()

if __name__ == "__main__":
    # cProfile.run('Main()')
    Main()
    # print('Cumulative Time',cumsum)
