import numpy as np
import cProfile
from collections import OrderedDict

''''
         20002241 function calls in 6.130 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.118    0.118 tnumpyhole.py:16(withnumpyhist)
        1    3.312    3.312    4.426    4.426 tnumpyhole.py:22(byhand)
        1    0.634    0.634    1.442    1.442 tnumpyhole.py:30(withnumpyunique)
'''

def withnumpyhist(x,mn,mx,nbins):
    binsize = (mx-mn) / nbins
    hist, bins = np.histogram(x, bins=nbins)
    sparsebins = {k:v for k,v in enumerate(hist) if v > 0}
    return sparsebins

def byhand(x,mn,mx,nbins):
    sparsebins = {}
    binsize = (mx-mn) / nbins
    keys = ((x - mn) // binsize).astype(int)
    for k in keys:
        sparsebins[k] = sparsebins.get(k,0) + 1
    return sparsebins

def withnumpyunique(x,mn,mx,nbins):
    max_value = mx # np.nanmax(x)
    min_value = mn # np.nanmin(x)
    bin_offset = min_value
    bin_size = (max_value - min_value)/nbins
    data = x
    freqs = np.ones(len(x), dtype = np.uint64)
    bins =  ((data-bin_offset) // bin_size).astype(int)
    sorted_idx = bins.argsort()
    group_bins, group_start_idx, counts = np.unique(bins[sorted_idx], return_index = True, return_counts = True)
    group_freqs = np.add.reduceat(freqs[sorted_idx], group_start_idx)
    sparsedict = {k:v for k,v in zip(group_bins, group_freqs)}
    return sparsedict



def main():
    xmin = 10
    xmax = 1500
    nelt = 10000000
    nbs = 1000
    x = np.concatenate((np.random.uniform(low=xmin,high=xmin+10,size=nelt),
                        np.random.uniform(low=xmax-10,high=xmax,size=nelt)))
    s1 = byhand(x,xmin,xmax,nbs)
    s2 = withnumpyunique(x,xmin,xmax,nbs)
    s3 = withnumpyhist(x,xmin,xmax,nbs)
    print(OrderedDict(sorted(s1.items())))
    print(OrderedDict(sorted(s2.items())))
    print(OrderedDict(sorted(s3.items())))

if __name__ == "__main__":
    cProfile.run('main()')


                   
