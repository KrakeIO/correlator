import csv
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
import operator

all_closes = {}
percents = {}

def read_csv():
	df = pd.read_csv('daily_trades.csv',
					   usecols = ['company_id', 'date_published', 'close'],
					   parse_dates = ['date_published'], infer_datetime_format = True)
	df = df.dropna()
	df['date_published'] = df['date_published'].apply(lambda x: x.date()).astype('datetime64[ns]')
	df.drop_duplicates(subset = ['company_id', 'date_published'], inplace = True)
	df.sort_values(by = ['company_id', 'date_published'], inplace = True)
	df = df.groupby('company_id')['date_published', 'close']
	global all_closes
	for name, group in df:
		all_closes[name] = group.set_index('date_published')['close'].to_dict()

def compute_long_percent():
	global percents
	for company, closes in all_closes.items():
		if company <= 1000:
			percents[company] = {}
			starting = datetime(2018, 3, 5)
			ending = datetime(2019, 7, 8)
			week = starting
			while week <= ending:
				first = None
				last = None
				if week in closes:
					first = week
				elif week + timedelta(1) in closes:
					first = week + timedelta(1)
				elif week + timedelta(2) in closes:
					first = week + timedelta(2)
				if week + timedelta(6) in closes:
					last = week + timedelta(6)
				elif week + timedelta(5) in closes:
					last = week + timedelta(5)
				elif week + timedelta(4) in closes:
					last = week + timedelta(4)
				if first != None and last != None:
					percents[company][week] = (closes[last] - closes[first]) / closes[first]
				week = week + timedelta(7)
	with open('long_percents.pickle', 'wb') as handle:
	    pickle.dump(percents, handle, protocol=pickle.HIGHEST_PROTOCOL)
	handle.close()

def compute_percents():
	global percents
	for company, closes in all_closes.items():
		for date in closes:
			percent = get_percent(date, closes)
			if (percent):
				if company not in percents:
					percents[company] = {}
				percents[company][date] = percent

	with open('percents.pickle', 'wb') as handle:
	    pickle.dump(percents, handle, protocol=pickle.HIGHEST_PROTOCOL)
	handle.close()

def get_percent(date, closes):
	if date - timedelta(1) in closes:
		return (closes[date] - closes[date - timedelta(1)]) / closes[date - timedelta(1)]
	else:
		return None

def load_percents():
	global percents
	with open('percents.pickle', 'rb') as handle:
	    percents = pickle.load(handle)
	handle.close()

def print_percents(company1, company2):
	sorted_percents = sorted(percents[company1].keys())
	for date in sorted_percents:
		if date in percents[company2]:
			print date, percents[company1][date], percents[company2][date]

def parse_weekly():
	get_period = lambda date: date - timedelta(date.weekday())
	get_day = lambda date: date.weekday()
	starting = datetime(2018, 3, 5)
	ending = datetime(2019, 7, 8)
	next_period = lambda week: week + timedelta(7)
	cutoff = 4
	export_name = "correlation_weekly.csv"
	parse(get_period, get_day, starting, ending, next_period, cutoff, export_name)

def parse_monthly():
	get_period = lambda date: datetime(date.year, date.month, 1)
	get_day = lambda date: date.day
	starting = datetime(2018, 3, 1)
	ending = datetime(2019, 7, 1)
	next_period = lambda month: datetime(month.year + (month.month / 12), (month.month % 12) + 1, 1)
	#cutoff = 15
	cutoff = 3
	export_name = "correlation_long_monthly.csv"
	parse(get_period, get_day, starting, ending, next_period, cutoff, export_name)

def parse_quarterly():
	get_period = lambda date: datetime(date.year, date.month - ((date.month - 1) % 3), 1)
	get_day = lambda date: (date - datetime(date.year, date.month - ((date.month - 1) % 3), 1)).days + 1
	starting = datetime(2018, 4, 1)
	ending = datetime(2019, 4, 1)
	next_period = lambda quarter: datetime(quarter.year + (quarter.month / 10), ((quarter.month + 2) % 12) + 1, 1)
	cutoff = 45
	export_name = "correlation_quarterly.csv"
	parse(get_period, get_day, starting, ending, next_period, cutoff, export_name)

def parse_yearly():
	get_period = lambda date: datetime(date.year, 1, 1)
	get_day = lambda date: (date - datetime(date.year, 1, 1)).days + 1
	starting = datetime(2018, 1, 1)
	ending = datetime(2019, 1, 1)
	next_period = lambda year: datetime(year.year + 1, 1, 1)
	cutoff = 200
	export_name = "correlation_yearly.csv"
	parse(get_period, get_day, starting, ending, next_period, cutoff, export_name)

def parse(get_period, get_day, starting, ending, next_period, cutoff, export_name):
	percents_clustered = {}
	for company, closes in percents.items():
		for date, close in closes.items():
			period = get_period(date)
			day = get_day(date)
			if company not in percents_clustered:
				percents_clustered[company] = {}
			if period not in percents_clustered[company]:
				percents_clustered[company][period] = {}
			percents_clustered[company][period][day] = percents[company][date]

	f = open(export_name, "w")
#	f.write('company1,company2,period,distance\n')

	for company1 in percents_clustered:
		print "analyzing company", company1
		for company2 in percents_clustered:
			if company1 <= 1000 and company2 <= 1000 and company1 < company2:
				period = starting
				while period <= ending:
					if period in percents_clustered[company1] and period in percents_clustered[company2]:
						data1 = percents_clustered[company1][period]
						data2 = percents_clustered[company2][period]
						common = set(data1.keys()).intersection(set(data2.keys()))
						if len(common) >= cutoff:
							shared1 = [data1[date] for date in common]
							shared2 = [data2[date] for date in common]
							distance = spatial.distance.cosine(shared1, shared2)
							f.write(('%d,%d,%s,%f\n') % (company1, company2, period, distance))
					period = next_period(period)

pdb.set_trace()
