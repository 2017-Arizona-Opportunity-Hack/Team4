import pandas as pd
import geocoder
import json

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
	if 'animal' in filter_dict:
		filters_missing.append(data_missing['Offer Method Animal'] == -1)
	if 'candy' in filter_dict:
		filters_missing.append(data_missing['Offer Method Candy'] == -1)
	if 'money' in filter_dict:
		filters_missing.append(data_missing['Offer Method Money'] == -1)
	if 'ride' in filter_dict:
		filters_missing.append(data_missing['Offer Method Ride'] == -1)
	if 'other' in filter_dict:
		filters_missing.append(data_missing['Offer Method Other'] == -1)
	if 'date_min' in filter_dict:
		#filters_missing.append(data_missing['Missing Date'] >= data_missing['Missing Date'].min(axis=0))
		filters_missing.append(data_missing['Missing Date'] >= filter_dict['date_min'])
	if 'date_max' in filter_dict:
		filters_missing.append(data_missing['Missing Date'] <= filter_dict['date_max'])
	print('Num filters being applied to missing:', len(filters_missing))

	compound_filter = None
	for i in range(len(filters_missing)):
		if type(compound_filter) == type(None):
			compound_filter = filters_missing[i]
		else:
			compound_filter = compound_filter & filters_missing[i]

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
		if 'state' in filter_dict:
			filters_attempt.append(data_attempt['Incident State'] == filter_dict['state'])
		if 'date_min' in filter_dict:
			#filters_attempt.append(data_attempt['Incident Date'] >= data_attempt['Incident Date'].min(axis=0))
			filters_attempt.append(data_attempt['Incident Date'] >= filter_dict['date_min'])
		if 'date_max' in filter_dict:
			filters_attempt.append(data_attempt['Incident Date'] <= filter_dict['date_max'])
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
	else:
		filtered_attempt = []
	print('num missing:', len(filtered_missing))
	print('num attempted:', len(filtered_attempt))

	return __collate_locations(filtered_missing, filtered_attempt)

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

if __name__ == "__main__":
	#print(load_all_data())
	#print(load_filtered_data({'gender':'Female', 'age_min':'1', 'age_max':'3'}))
	#locations = load_filtered_data({'date_min':'2011-01-01', 'date_max':'2014-01-01', 'location':'6161 e grant rd tucson az 85712', 'location_range':'50'})
	locations = load_filtered_data({'gender':'Female', 'location':'6161 e grant rd tucson az 85712', 'location_range':'50'})
	print(len(locations))
	print(locations[0])
