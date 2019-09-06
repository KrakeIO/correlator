import numpy
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pickle
# import random
import statistics
import pdb

with open('correlation.pickle', 'rb') as handle:
    correlation = pickle.load(handle)
print len(correlation)
means = {}
variances = {}
for pair in correlation:
	if len(correlation[pair]) > 1:
		mean = statistics.mean(correlation[pair].values())
 		means[pair] = mean
 		variances[pair] = statistics.stdev(correlation[pair].values()) / mean
plt.scatter(means.values(), variances.values(), 1)
plt.show()

# x = []
# y = []

# for a in range(100000):
# 	c = random.randint(1,100000)
# 	y.append(random.randint(1,c))
# 	x.append(c)

# plt.scatter(x, y, s = 1)
# plt.show()
