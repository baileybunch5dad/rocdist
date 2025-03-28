from statsmodels.stats.weightstats import DescrStatsW
import numpy as np
from DynamicDist import DynamicDist

data = np.random.uniform(low=0, high=100, size=1000) # sample size
moredata = np.random.uniform(low=99,high=100, size=1000000)
rd = DynamicDist()
rd.add_many(data)
rd.add_many(moredata)
hist, bins = np.histogram(data, bins=100)
hist, bins = rd.histogram(np.concatenate((data, moredata), n_bins=100)
quantiles = np.linspace(0.01,.0.99,)

def compare_to_numpy(rd, bigarray: np.array):
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
    print(elapsed, type(rd).__name__)
    nhist, nbins = np.histogram(bigarray, bins=n_bins)
    return hist, bins, nhist, nbins
    
    return compare_to_numpy(rd, vals)

# Define some data and their probabilities
data = [1, 2, 3, 4, 5, 6]
probabilities = [0.25, 0.05, 0.1, 0.3, 0.02, 0.1]
# Create a weighted statistics object:
stats = DescrStatsW(data, weights = probabilities)# Compute the quantiles
stats.quantile([0.10, 0.25, 0.50, 0.75, 0.90])