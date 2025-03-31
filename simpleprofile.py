from DynamicDist import DynamicDist
import numpy as np
import cProfile

def main():
    rd = DynamicDist()
    vals = np.random.uniform(low=0, high=100, size=100000000)
    for v in vals:
        rd.add(v)
    hist, bins = rd.histogram()
    
if __name__=="__main__":
    cProfile.run('main()')
