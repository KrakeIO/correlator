import pickle
import numpy
import matplotlib.pyplot as plt

with open('data.pickle', 'rb') as handle:
    data = pickle.load(handle)
    plt.plot(data[5980])
    plt.plot(data[6578])
    plt.figure()
    plt.plot(data[4094])
    plt.plot(data[3892])
    plt.plot(data[478])
    plt.plot(data[4438])
    plt.show()