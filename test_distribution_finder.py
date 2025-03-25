import pytest
from rocdist import RocDist
import math
import numpy as np
from DynamicDist import DynamicDist
from FixedArrayDist import FastDist

def getDist():
    # return DynamicDist()
    # return RocDist()
    return FastDist()

# for 0 and 1 value, match numpy histogram exactly
def test_no_values(): 
    rd = getDist()
    vals = np.array([])
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

# single value in numpy is weird, 
# makes 10 buckets with binwidth 0.1
# but whatever, make it match
def test_single_value():
    rd = getDist()
    vals = np.array([17.])
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_single_missing_value(): # nan count is singleton on far left
    rd = getDist()
    vals = np.array([np.nan])
    with pytest.raises(ValueError):
        for v in vals:
            rd.add(v)
        rochist, rocbins = rd.histogram()
    with pytest.raises(ValueError):
        nphist, npbins = np.histogram(vals, bins=100)

def test_repeat_single_value():
    rd = getDist()
    vals = np.repeat(17,5)
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_ten_evenly_spaced():
    rd = getDist()
    vals = np.arange(25,35)
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_repeated_groups_of_ten():
    rd = getDist()
    vals = np.arange(25,35)
    vals = np.tile(vals,3).flatten()
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_draws_from_random_normal():    
    rd = getDist()
    mu = 17
    sigma = 2
    vals = np.random.normal(loc=mu, scale=sigma, size=100)
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_large_normal():
    rd = getDist()
    mu = 1000
    sigma = 300
    vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_late_growth():
    rd = getDist()
    sigma = 2
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        for v in vals:
            rd.add(v)
    rochist, rocbins = rd.histogram()
    assert(len(rochist) > 10)
    assert(len(rocbins) > 10)

def test_sparse_multiple_groups():
    rd = getDist()
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
    # if hist is None:
    #     mid, cnt = rd.sparsehist()
    #     assert(len(mid) > 10)
    #     assert(len(cnt) > 10)

