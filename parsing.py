import csv
from datetime import datetime
from datetime import timedelta
import pickle

start = '2019-04-01'
end = '2019-05-31' # inclusive

with open('daily_trades.csv') as file:
	reader = csv.reader(file, delimiter=",")
	data = {}
	first_row = True
	date_format = "%Y-%m-%d"
	starting_date = datetime.strptime(start, date_format) - timedelta(1)
	size = (datetime.strptime(end, date_format) - starting_date).days + 1
	for row in reader:
		if first_row == False:
			company_id = int(row[1])
			date_string = row[5][:10]
			date = datetime.strptime(date_string, date_format)
			day = (date - starting_date).days
			close_string = str(row[8])
			try:
				close = float(close_string)
			except ValueError,e:
				print close
			if company_id not in data:
				data[company_id] = [None] * size
			if day >= 0 and day < size:
				data[company_id][day] = close
		else:
			first_row = False
	invalid = []
	for company_id in data:
		if None in data[company_id]:
			invalid.append(company_id)
	for company_id in invalid:
		del data[company_id]
	print len(data), "valid companies"

with open('data.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

f = open("ids.txt", "w+")
f.truncate()
for company_id in data:
	f.write("%f\r\n" % company_id)
f.close()

