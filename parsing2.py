import pandas as pd
import pdb
from datetime import datetime
from datetime import timedelta
from scipy import spatial
import pickle
import numpy
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import statistics
import json

# df = pd.read_csv('daily_trades.csv',
# 				   usecols = ['company_id', 'date_published', 'close'],
# 				   parse_dates = ['date_published'], infer_datetime_format = True)
# df = df.dropna()
# df['date_published'] = df['date_published'].apply(lambda x: x.date()).astype('datetime64[ns]')
# df.drop_duplicates(subset = ['company_id', 'date_published'], inplace = True)
# df.sort_values(by = ['company_id', 'date_published'], inplace = True)
# df = df.groupby('company_id')['date_published', 'close']
# all_closes = {}
# for name, group in df:
# 	all_closes[name] = group.set_index('date_published')['close'].to_dict()

# print "initial phase done"

# def get_percent(date, closes):
# 	if date - timedelta(1) in closes:
# 		return (closes[date] - closes[date - timedelta(1)]) / closes[date - timedelta(1)]
# 	else:
# 		return None

# percents = {}
# for company, closes in all_closes.items():
# 	for date in closes:
# 		percent = get_percent(date, closes)
# 		if (percent):
# 			month = datetime(date.year, date.month, 1)
# 			day = date.day
# 			if company not in percents:
# 				percents[company] = {}
# 			if month not in percents[company]:
# 				percents[company][month] = {}
# 			percents[company][month][date.day] = percent

# with open('percents.pickle', 'wb') as handle:
#     pickle.dump(percents, handle, protocol=pickle.HIGHEST_PROTOCOL)

# print "converted to percents"

# correlation = pd.DataFrame(columns=['company1', 'company2', 'month', 'distance'])
correlation = {}

starting = datetime(2018, 3, 1)
ending = datetime(2019, 7, 1)

with open('percents.pickle', 'rb') as handle:
    percents = pickle.load(handle)
handle.close()

f = open("correlation.csv", "a")
# f.write('company1,company2,month,distance\n')

for company1 in percents:
	print "analyzing company", company1
	for company2 in percents:
		# print "analyzing company", company1, company2
		if company1 >= 597 and company1 <= 1000 and company1 < company2:
			# pair = (company1, company2)
			# correlation[company1] = {}
			month = starting
			while month <= ending:
				# print month
				if month in percents[company1] and month in percents[company2]:
					data1 = percents[company1][month]
					data2 = percents[company2][month]
					common = set(data1.keys()).intersection(set(data2.keys()))
					if len(common) >= 10:
						# print "match"
						shared1 = [data1[date] for date in common]
						shared2 = [data2[date] for date in common]
						distance = spatial.distance.cosine(shared1, shared2)
						f.write(('%d,%d,%s,%f\n') % (company1, company2, month, distance))
						# correlation[pair][month] = spatial.distance.cosine(shared1, shared2)
						# correlation = correlation.append({'company1':company1, 'company2':company2, 'month':month, 'distance':spatial.distance.cosine(shared1, shared2)}, ignore_index = True)
				month = datetime(month.year + (month.month / 12), (month.month % 12) + 1, 1)



# print correlation
print "done analyzing"

# means = {}
# variances = {}
# for pair in correlation:
# 	if len(correlation[pair]) > 1:
# 		mean = statistics.mean(correlation[pair].values())
#  		means[pair] = mean
#  		variances[pair] = statistics.stdev(correlation[pair].values()) / mean
# pdb.set_trace()
# plt.scatter(means.values(), variances.values(), 1)
# plt.show()
# with open('correlation2.pickle', 'wb') as handle:
#     pickle.dump(correlation, handle, protocol=pickle.HIGHEST_PROTOCOL)
# handle.close()


# file2 = 
# print(file2.head(5))
# pdb.set_trace();