import os
import datetime
import pandas as pd
import geocoder
import json
import numpy as np
import matplotlib.pyplot as plt

def load_filtered_data(filter_dict):
	'''
	Return tuple containing whether or not the abduction was successful and
	latitude/longitude coordinates of cases that conform to the parameters in
	the filter dictionary obtained .

	(crime_success, (latitude, longitude))
	'''
	missing_data_filename = 'Hackathon_Missing_Child_5_Years_of_Data_Geo.csv'
	attempt_data_filename = 'Attempts_Hackathon_5_Years_of_Data_Geo.csv'

	try:
		data_missing = pd.read_csv(missing_data_filename)
	except:
		print('Error attempting to open {0}'.format(missing_data_filename))
		return []

	try:
		data_attempt = pd.read_csv(attempt_data_filename)
	except:
		print('Error attempting to open {0}'.format(attempt_data_filename))
		return []

	pi = 3.141592654
	R = 3959

	test_lat_lon = (40.1, -75.38)
	#test_lat_lon = ((test_lat_lon[0]), (test_lat_lon[1]))

	filters_missing = []
	# Assumes that the location range parameter is in miles.
	# Small angle approximation to convert a mile distance to angles on a
	# perfect sphere of radius R.
	# This allows us to get lat/longs within a square area of a specified
	# location.
	if 'location' in filter_dict and 'location_range' in filter_dict:
		#start_lat_lon = geocoder.google(filter_dict['location']).latlng
		#if start_lat_lon == [] or type(start_lat_lon) == type(None):
		#	start_lat_lon = test_lat_lon

		location_range = float(filter_dict['location_range'])
		delta_theta = location_range/R

		lat_max = start_lat_lon[0] + delta_theta*180/pi
		lat_min = start_lat_lon[0] - delta_theta*180/pi

		lon_max = start_lat_lon[1] + delta_theta*180/pi
		lon_min = start_lat_lon[1] - delta_theta*180/pi

		filters_missing.append(data_missing['Lat'] >= lat_min)
		filters_missing.append(data_missing['Lat'] <= lat_max)

		filters_missing.append(data_missing['Lon'] >= lon_min)
		filters_missing.append(data_missing['Lon'] <= lon_max)

		print('Angular search range:')
		print('Lat:', lat_max, lat_min)
		print('Lon:', lon_max, lon_min)

	if 'gender' in filter_dict:
		if filter_dict['gender'] != 'All':
			filters_missing.append(data_missing['Gender'] == filter_dict['gender'])
	if 'state' in filter_dict:
		filters_missing.append(data_missing['Missing State'] == filter_dict['state'])
	if 'age_min' in filter_dict:
		#filters_missing.append(data_missing['Age Missing'] >= data_missing['Age Missing'].min(axis=0))
		filters_missing.append(data_missing['Age Missing'] >= int(filter_dict['age_min']))
	if 'age_max' in filter_dict:
		#filters_missing.append(data_missing['Age Missing'] <= data_missing['Age Missing'].max(axis=0))
		filters_missing.append(data_missing['Age Missing'] <= int(filter_dict['age_max']))
	if 'date_min' in filter_dict:
		date_min = convert_date(filter_dict['date_min'])
		#filters_missing.append(data_missing['Missing Date'] >= data_missing['Missing Date'].min(axis=0))
		filters_missing.append(data_missing['Missing Date'] >= date_min)
	if 'date_max' in filter_dict:
		date_max = convert_date(filter_dict['date_max'])
		filters_missing.append(data_missing['Missing Date'] <= date_max)
	print('Num filters being applied to missing:', len(filters_missing))

	compound_filter = None
	for i in range(len(filters_missing)):
		if type(compound_filter) == type(None):
			compound_filter = filters_missing[i]
		else:
			compound_filter = compound_filter & filters_missing[i]

	if len(filters_missing) == 0:
		filtered_missing = data_missing[['Lat', 'Lon']].values.tolist()
	else:
		filtered_missing = data_missing[compound_filter][['Lat', 'Lon']].values.tolist()

	filters_attempt = []
	display_attempt = True
	for lure in ['animal', 'candy', 'money', 'ride', 'other']:
		if lure in filter_dict:
			display_attempt = False
			print('Found lure in filters')
			break
	if display_attempt:
		if 'location' in filter_dict and 'location_range' in filter_dict:
			start_lat_lon = geocoder.google(filter_dict['location']).latlng
			if start_lat_lon == []:
				start_lat_lon = test_lat_lon
			location_range = float(filter_dict['location_range'])
			delta_theta = location_range/R

			lat_max = start_lat_lon[0] + delta_theta*180/pi
			lat_min = start_lat_lon[0] - delta_theta*180/pi

			lon_max = start_lat_lon[1] + delta_theta*180/pi
			lon_min = start_lat_lon[1] - delta_theta*180/pi

			filters_attempt.append(data_attempt['Lat'] >= lat_min)
			filters_attempt.append(data_attempt['Lat'] <= lat_max)

			filters_attempt.append(data_attempt['Lon'] >= lon_min)
			filters_attempt.append(data_attempt['Lon'] <= lon_max)

		if 'gender' in filter_dict:
			compound_filter = None
			if filter_dict['gender'] != 'All':
				for i in range(6):
					gender_filter = data_attempt['Child Gender ' + str(i + 1)] == filter_dict['gender']
					if type(compound_filter) == type(None):
						compound_filter = gender_filter
					else:
						compound_filter = compound_filter | gender_filter
			filters_attempt.append(compound_filter)
		age_min = 0
		age_max = 21
		if 'age_min' in filter_dict:
			age_min = int(filter_dict['age_min'])
		if 'age_max' in filter_dict:
			age_max = int(filter_dict['age_max'])
		compound_filter = None
		for i in range(6):
			age_range_filter = (data_attempt['Child Perceived Age ' + str(i + 1)] >= str(age_min)) & \
				(data_attempt['Child Perceived Age ' + str(i + 1)] <= str(age_max))
			if type(compound_filter) == type(None):
				compound_filter = age_range_filter
			else:
				compound_filter = compound_filter | age_range_filter
			filters_attempt.append(compound_filter)
		if 'state' in filter_dict:
			filters_attempt.append(data_attempt['Incident State'] == filter_dict['state'])
		if 'date_min' in filter_dict:
			#filters_attempt.append(data_attempt['Incident Date'] >= data_attempt['Incident Date'].min(axis=0))
			#date_min = '-'.join(filter_dict['date_min'].split('/'))
			date_min = convert_date(filter_dict['date_min'])
			filters_attempt.append(data_attempt['Incident Date'] >= date_min)
		if 'date_max' in filter_dict:
			date_max = convert_date(filter_dict['date_max'])
			filters_attempt.append(data_attempt['Incident Date'] <= date_max)

		if 'animal' in filter_dict:
			filters_attempt.append(data_attempt['Offender Method Animal'] == -1)
		if 'candy' in filter_dict:
			filters_attempt.append(data_attempt['Offender Method Candy'] == -1)
		if 'money' in filter_dict:
			filters_attempt.append(data_attempt['Offender Method Money'] == -1)
		if 'ride' in filter_dict:
			filters_attempt.append(data_attempt['Offender Method Ride'] == -1)
		if 'other' in filter_dict:
			filters_attempt.append(data_attempt['Offender Method Other'] == -1)

		print('Num filters being applied to attempts:', len(filters_attempt))
		
		compound_filter = None
		for i in range(len(filters_attempt)):
			if type(compound_filter) == type(None):
				compound_filter = filters_attempt[i]
			else:
				compound_filter = compound_filter & filters_attempt[i]

		if len(filters_attempt) == 0:
			filtered_attempt = data_attempt[['Lat', 'Lon']].values.tolist()
		#stuff = data_attempt[compound_filter][['Lat', 'Lon']]
		else:
			filtered_attempt = data_attempt[compound_filter][['Lat', 'Lon']].dropna(axis=0, how='any').values.tolist()
			lure_frequency(data_attempt[compound_filter])
			time_of_day_breakdown(data_attempt[compound_filter])
	else:
		filtered_attempt = []

	print('num missing with current filter:', len(filtered_missing))
	print('num attempted with current filter:', len(filtered_attempt))

	return __collate_locations(filtered_attempt, filtered_missing)

def convert_date(date):
	(m, d, y) = date.split('/')
	m = "%02d" % (int(m),)
	d = "%02d" % (int(d),)
	date = [y, m, d]
	return '-'.join(date)

def load_all_data():
	'''
	Load all of the latitude/longitude coordinates for every row in each
	dataset.
	'''

	missing_data_filename = 'Hackathon_Missing_Child_5_Years_of_Data_Geo.csv'
	attempt_data_filename = 'Attempts_Hackathon_5_Years_of_Data_Geo.csv'

	try:
		data_missing = pd.read_csv(missing_data_filename)
	except:
		print('Error attempting to open {0}'.format(missing_data_filename))
		return []

	try:
		data_attempt = pd.read_csv(attempt_data_filename)
	except:
		print('Error attempting to open {0}'.format(attempt_data_filename))
		return []

	attempt_locations = data_attempt[['Lat', 'Lon']].values.tolist()
	missing_locations = data_missing[['Lat', 'Lon']].values.tolist()

	return __collate_locations(attempt_locations, missing_locations)


def __collate_locations(set1, set2):
	'''
	Takes in two lists of (lat, long) tuples and puts them into a single list
	of tuples of the form (attempt_success, (lat, long)), where attempt_success
	is an integer (0 for an attempt, 1 for missing).
	'''

	locations = [(0, tuple(i)) for i in set1] + [(1, tuple(i)) for i in set2]
	return locations

def lure_frequency(filtered_attempt):
	'''
	Counts up the number of times each lure is used without paying attention to
	combinations of lures being used at once.
	'''

	image_name = os.path.join('static', 'images', 'lure_info.png')
	lure_columns = [i for i in list(filtered_attempt)
		if 'offender method' in i.lower() and 'detail' not in i.lower()]
	# Just counts up the number of times a particular lure is used.
	lure_data = {key: sum([1 for i in filtered_attempt[key].tolist()
		if i == -1]) for key in lure_columns}
	num_lures_used = sum(list(lure_data.values()))

	# Normalizes the counts of the lure data against the total number of lures used.
	#lure_data = {key: lure_data[key]/num_lures_used for key in lure_data}
	
	labels = [m.split()[-1] for m in lure_columns]
	y_vals = [lure_data[key] for key in lure_columns]
	x_vals = [i for i in range(len(y_vals))]
	plt.bar(x_vals, y_vals)
	plt.xticks(x_vals, labels, rotation='vertical')
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.15)
	plt.title('Most common lures for current filter')
	plt.savefig(image_name)
	plt.close()

	return image_name

def time_of_day_breakdown(filtered_attempt):
	'''
	Produces a breakdown of the frequency of incidents for time of day and day
	of week for the current filter status.
	'''

	image_name = os.path.join('static', 'images', 'day_time_stats.png')

	day_labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	time_labels = [str(i) for i in range(24)]

	counts_2d = np.zeros((24, 7))
	num_rows = filtered_attempt.shape[0]
	x = []
	y = []

	for i in range(num_rows):
		row_date = filtered_attempt['Incident Date'].iloc[i]
		row_time = filtered_attempt['Incident Time'].iloc[i]
		dow = datetime.datetime.strptime(row_date, "%Y-%m-%d").strftime("%A")
		tod = int(int(row_time)/100)
		counts_2d[tod, day_labels.index(dow)] += 1.0
		if tod > 0:
			y.append(tod)
			x.append(day_labels.index(dow))

	x = np.array(x)
	y = np.array(y)

	counts_2d = counts_2d[1:, :]
	print(counts_2d)
	plt.scatter(x, y, alpha=1/counts_2d.max(), s=400)
	plt.xticks(range(7), day_labels, rotation=-45)
	plt.margins(0.2)
	plt.ylabel('Time of day')
	plt.title('Incident frequency for time of day and day of week ' + \
		'\nfor current filter selection')
	plt.subplots_adjust(bottom=0.15)
	plt.savefig(image_name)
	plt.close()

if __name__ == "__main__":
	#print(load_all_data())
	#print(load_filtered_data({'gender':'Female', 'age_min':'1', 'age_max':'3'}))
	locations = load_filtered_data({})
	#locations = load_filtered_data({'date_min':'2011-01-01', 'date_max':'2014-01-01', 'location':'6161 e grant rd tucson az 85712', 'location_range':'50'})
	#locations = load_filtered_data({'gender':'Female', 'location':'6161 e grant rd tucson az 85712', 'location_range':'50'})
	print(len(locations))
	print(locations[0])
