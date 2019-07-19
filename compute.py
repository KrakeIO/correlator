import pickle
from scipy import spatial
import operator
import numpy
import matplotlib.pyplot as plt

with open('data.pickle', 'rb') as handle:
    data = pickle.load(handle)
    data2 = {}
    for company_id in data:
    	values = data[company_id]
    	deltas = [None] * (len(values) - 1)
    	for i in range(len(values) - 1):
    		deltas[i] = (values[i+1] - values[i]) / values[i]
    	data2[company_id] = deltas

    company = 970
    a = data2[company]

    distances = {}

    for company_id in data:
    	if company_id != company:
    		b = data2[company_id]
    		result = spatial.distance.cosine(a, b)
    		distances[company_id] = result

    sorted_distances = sorted(distances, key=distances.get)

    print "Top 5"
    plt.plot(data[company], label = company)
    for i in range(5):
    	company_id = sorted_distances[i]
    	print company_id, ":", distances[company_id]
    	plt.plot(data[company_id], label = company_id)
    plt.legend()
    plt.figure()

    print "Bottom 5"
    plt.plot(data[company], label = company)
    for i in range(5):
    	company_id = sorted_distances[len(sorted_distances) - i - 1]
    	print company_id, ":", distances[company_id]
    	plt.plot(data[company_id], label = company_id)
    plt.legend()
    plt.show()
