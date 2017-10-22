import pandas as pd

data_missing = pd.read_csv('Hackathon_Missing_Child_5_Years_of_Data.csv')
data_attempt = pd.read_csv('Attempts_Hackathon_5_Years_of_Data.csv')

#data_missing = data_missing[data_missing.name.notnull()]
#data_attempt = data_attempt[data_attempt.name.notnull()]

def get_addresses():
	columns_missing = ['Missing City', 'Missing State', 'Missing Zip']
	columns_attempt = ['Incident Location', 'Incident City', 'Incident State', 'Incident Zip']

	attempt_locations_raw = data_attempt[columns_attempt]

	num_bad_zips = 0

	locations = []
	print(len(data_attempt))
	for i in range(len(data_attempt)):
		location = list(attempt_locations_raw.iloc[i])

		try:
			# Zip codes are pulled down as floats
			location[-1] = str(int(location[-1]))
		except:
			#print('Ran across a NaN zip code. No worries, I\'ll ignore it.')
			#print('It was at row {0}, btw.'.format(i))
			location = location[0:-1]
			num_bad_zips += 1

		if (i*100/(int(len(data_attempt)/10)*10) % 10 == 0):
			print('{0}% finished'.format(i/len(data_attempt)*100))

		if 'unknown' not in location[0].lower():
			locations.append(' '.join(location))

	print('\n\tTotal number of bad zip codes:', num_bad_zips)

	return locations

if __name__ == '__main__':
	locs = get_addresses()
	print(locs[0])
	print(locs[100])
	print(locs[205])