from statsmodels.stats.weightstats import DescrStatsW
import numpy as np
from DynamicDist import DynamicDist

n_bins: int = 1000
buffer_size: int = 100000

sample = np.random.uniform(low=0, high=100, size=buffer_size) # sample size
additional = np.full((1000000), 1-1e-3)
rd = DynamicDist(n_bins=n_bins, buffer_size=buffer_size)
rd.add_many(sample)
rd.add_many(additional)
alldata = np.concatenate((sample,additional))

mean = np.mean(alldata)
median = np.median(alldata)

n_bins = 100
hist, bins = rd.histogram(n_bins=n_bins)
bins = np.append(bins, bins[-1] + (bins[1]-bins[0])) # make Rocco bins match numpy bins
# hist, bins = np.histogram(alldata, bins=100)
binWidth = bins[1] - bins[0]
dswData = bins[:-1] + binWidth/2
dswWeights = hist/hist.sum()
dsw = DescrStatsW(dswData, weights=dswWeights)
dswMean = dsw.mean

maxError = (bins[-1] - bins[0]) /  (2 * n_bins)
actError = np.abs(dswMean - mean)
print(f'{median=}\n{mean=}\n{dswMean=}\n{maxError=}\n{actError=}')


