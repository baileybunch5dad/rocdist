from rocdist import RocDist
import numpy as np
import matplotlib.pyplot as plt

def plot_sparse():
    rd = RocDist()
    sigma = 2
    for mu in range(27,48,10):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        for v in vals:
            rd.add(v)
    for mu in range(4000,80000,1000):
        vals = np.random.normal(loc=mu, scale=sigma, size=100000)
        for v in vals:
            rd.add(v)
    mid, cnt = rd.sparsehist()
    plt.plot(mid,cnt)
    plt.show()

if __name__=="__main__":

    # Data for the plot
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 1, 3, 5]

    # Create the plot
    plt.plot(x, y)

    # Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Hello, World! Plot")

    # Display the plot
    plt.show()

    # plot_sparse()
