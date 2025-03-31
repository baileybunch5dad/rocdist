from DynamicDist import DynamicDist
import numpy as np
import cProfile

def testnumpy():
    bigarray = np.empty((0))
    for i in range(1):
        vals = np.random.uniform(low=0, high=100, size=100000000)
        bigarray = np.concatenate((bigarray, vals), axis=0)
    hist, bins = np.histogram(bigarray)
    pass

def testdd():
    rd = DynamicDist()
    for i in range(1):
        vals = np.random.uniform(low=0, high=100, size=100000000)
        rd.add_many(vals)
    # hist, bins = rd.histogram()
    

def main():
    testnumpy()
    testdd()
    
if __name__=="__main__":
    cProfile.run('main()')
