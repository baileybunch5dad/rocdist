from SparseDist import SparseDist
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FixedArrayDist
from time import perf_counter
import cProfile
import matplotlib.pyplot as plt
import inspect
from matplotlib.axes import Axes


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
# for an algorithm and some data get the results, the time, and the error
#
def results_time_error(algorithm, bigarray: np.array, actualhist: np.array, actualbins: np.array):
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
    print(f'{type(algorithm).__name__} Time={elapsed:.1f} RMSE={rmse:.1f}')
    return predhist, predbins, elapsed, rmse
    

#
# Compare an algorithm that does not hold the entire data and must 'estimate'
# an a given data set by refining a sample to something that hold the entire data
#    
def compare_to_numpy(ax, testfcn):
    testname = testfcn.__name__
    bigarray = testfcn()
    # testname = inspect.stack()[1] # name of calling function
    actualhist, actualbins = np.histogram(bigarray, bins=100)
    dhist, dbins, dtime, derr = results_time_error(DynamicDist(), bigarray, actualhist, actualbins)
    shist, sbins, stime, serr = results_time_error(SparseDist(), bigarray, actualhist, actualbins)
    # Overlay the hisogram of the predictor versus the actual
    ax.stairs(actualhist, actualbins, label='numpy')
    ax.stairs(dhist, dbins, label=f'DynamicDist T={dtime:.1f}s RMSE={derr:.1f}' )
    ax.stairs(shist, sbins, label=f'SparseDist  T={stime:.1f}s RMSE={serr:.1f}' )
    ax.set_title(f'{testname}')
    ax.legend()

# uniform distribution
def test_uniform():
    return np.random.uniform(low=0, high=100, size=100000000)

# 1,2,3 increasing
def test_monotonic():
    return np.sort(np.random.uniform(low=0, high=100, size=100000000))

# 1,2,3    100,101,102,   
def test_groups():
    sigma = 5
    bigarray = np.empty((0))
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    sigma = 700
    for mu in range(4000,40000,200): # add to the right
        vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    return bigarray

# 1, -1, 2, -2, 3, -3, ...
def test_oscillating():
    bigarray = np.linspace(1,1000,50000000)
    return np.array([bigarray,-bigarray]).T.ravel()

def Main():
    fig, axs = plt.subplots(2, 2)
    compare_to_numpy(axs[0,0], test_uniform)
    compare_to_numpy(axs[0,1], test_monotonic)
    compare_to_numpy(axs[1,0], test_groups)
    compare_to_numpy(axs[1,1], test_oscillating)
    plt.show()

if __name__ == "__main__":
    # cProfile.run('Main()')
    Main()
