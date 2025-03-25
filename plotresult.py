from FixedArrayDist import FastDist
from DynamicDist import DynamicDist
import numpy as np
import matplotlib.pyplot as plt

# NOTE: This will not display in WSL

def plot_overlay():
    rd = FastDist()
    mu = 1000
    sigma = 300
    vals = np.random.normal(loc=mu, scale=sigma, size=1000000)
    for v in vals:
        rd.add(v)
    rochist, rocbins = rd.histogram()
    nphist, npbins = np.histogram(vals, bins=100)
    plt.stairs(rochist, rocbins, label='FastDist')
    plt.stairs(nphist, npbins, label='numpy')
    plt.legend(loc='upper right')
    plt.show()

if __name__=="__main__":
    plot_overlay() 
