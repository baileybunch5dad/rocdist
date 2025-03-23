# rocdist

Rocco's Zero Sort Low Memory Distribution Finder

### Author: Rocco Cannizzaro
### Typist: Chris

the algorithm has as its basic requirement to be faster and use much less memory
than numpy.histogram, which requires all values in memory and then to be sorted

## Usage

```
rd = RocDist()
while True:
    rd.add(yetAnotherValue)
hist, bins = rd.histogram()
```

Following numpy.histogram return code convention
 All but the last (righthand-most) bin is half-open. 


## Algorithm

Collect a few samples, make bins based on them with counts at a small threshold
o(1) insertion during initial phase, add same width bins as needed on later growth

On insertion of a new element, just increment the count in the appropriate bucket if it fit, o(1)
if it does not fit, allocate new bucket of previous width to that and, and dup into new structure, o(n)

Iif has "normalized" distribution, algorithm will be o(n) rather than o(nlogn) of numpy histogram
 and at the same time, use only a single array of size nbuckets, so extremely low memory

Much of the code is dedicated to pathological case detection not needed in numpy.histogram, 
against which this is compared for correctness

If the number of buckets would grow by an exorbitant amount,
 for example if the input contained a repeated value setting the bucket width to zero,
 or similarly some tightly clustered values, then got values "relatively" far away 
 (based on number of bins it would have to create of that identical size)
 throw an error if growth amount greater than some threshold (alternatively rescale the existing buckets) 
 for example, if there were millions of random numbers between 0 and 1,
 and a hundred buckets were made to hold the counts of numbers 0.00<=x<0.001, 0.01<=x<0.02
 then another number comes in like 1e15 that with the original binWidth of 0.01 would cause an explosion
 return the exception

 Next pathological case is all value are identical

 Next pathological case is identical valuers initially (binwidth=0) in initial sample size
 followed by differing values
 detect this condition by range detection on initial sample
 
 Next pathological case is different distributions in data, for example two normal 
 distribution with different center and scale that the intial is received prior to the latter
 similar handling to pathological clustering

 Also pathological, like quicksort, is when data are sorted, combined with a low number of initial bins.
 This could cause growth to hit the limit and prematurely raise an exception.

 