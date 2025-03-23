import pytest
from rocdist import RocDist
import math
import numpy as np

# for 0 and 1 value, match numpy histogram exactly
def test_no_values(): 
    vals = np.array([])
    rd = RocDist()
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
    vals = np.array([17.])
    rd = RocDist()
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))

def test_single_missing_value():
    vals = np.array([np.nan])
    rd = RocDist()
    for v in vals:
        rd.add(v)
    with pytest.raises(ValueError):
        rochist, rocbins = rd.histogram()
    with pytest.raises(ValueError):
        nphist, npbins = np.histogram(vals)

def test_repeat_single_value():
    vals = np.repeat(17,5)
    rd = RocDist()
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals)
    assert(np.array_equal(rochist, nphist))
    assert(np.array_equal(rocbins, npbins))
