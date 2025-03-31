from DynamicDist import DynamicDist
import numpy as np
import cProfile

def main():
    # outliers at end during buffer sample
    rd = DynamicDist()
    bigarray = np.concatenate(( np.array([10000]), np.random.uniform(low=0, high=10, size=200000)))
    rd.add_many(bigarray)
    rd.add_many(bigarray)
    hist, bins = rd.histogram()
    print(f'{hist=} {bins=}')
    
    # rd = DynamicDist()
    # bigarray = np.concatenate(( np.array([10000]), np.random.uniform(low=0, high=10, size=200000)))
    # rd.add_many(np.random.uniform(low=0, high=10, size=100000)) # use Dist's buffer size
    # minval = -9
    # maxval = 1e6
    # rd.add(minval) # index -1
    # rd.add(maxval) # index max
    # rd.add_many(np.random.uniform(low=maxval/2, high=maxval/2+10, size=100000))
    # # rd.add_many(bigarray)
    # hist, bins = rd.histogram()
    # print(f'{hist=} {bins=}')
    
    # outliers at other end during buffer sample
    # rd = DynamicDist()
    # bigarray = np.concatenate((np.random.uniform(low=0, high=10, size=200000),  np.array([10000])))
    # rd.add_many(bigarray)
    # rd.add_many(bigarray)
    # hist, bins = rd.histogram()
    # print(f'{hist=} {bins=}')
    
    # outlier at right end after buffer sample
    
    
if __name__=="__main__":
    main()
    # cProfile.run('main()')
