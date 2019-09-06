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
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

all_closes = {}

def parse(limit):
	df = pd.read_csv('daily_trades.csv',
				   	 usecols = ['company_id', 'date_published', 'close'],
				     parse_dates = ['date_published'], infer_datetime_format = True)
	df = df.dropna()
	df['date_published'] = df['date_published'].apply(lambda x: x.date()).astype('datetime64[ns]')
	df.drop_duplicates(subset = ['company_id', 'date_published'], inplace = True)
	df = df[(df.company_id <= limit)]
	df.sort_values(by = ['company_id', 'date_published'], inplace = True)
	df = df.groupby('company_id')['date_published', 'close']
	global all_closes
	for name, group in df:
		all_closes[name] = group.set_index('date_published')['close'].to_dict()
	with open('closes.pickle', 'wb') as handle:
		pickle.dump(all_closes, handle, protocol=pickle.HIGHEST_PROTOCOL)
	handle.close()

def load():
	with open('closes.pickle', 'rb') as handle:
		global all_closes
		all_closes = pickle.load(handle)
	handle.close()

def graph_all(companies):
	graph(companies,datetime(2018,5,1),datetime(2019,8,1))

def graph(companies, start, end):
	print companies
	companies = list(filter(lambda x: x in all_closes.keys(), companies))
	print companies
	plt.figure()
	for company in companies:
		print company
		dates = list(filter(lambda x: x >= start and x < end, all_closes[company].keys()))
		dates.sort()
		closes = [all_closes[company][date] for date in dates]	
		# print dates
		# print closes
		plt.plot(dates, closes, label = company)
	plt.legend()
	plt.show()

pdb.set_trace()