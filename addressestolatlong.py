import csv
import pandas
import geocoder
from collections import defaultdict

with open('Attempts_Hackathon_5_Years_of_Data2.csv', 'rb') as csvFile:
	reader = csv.DictReader(csvFile)
	with open('Attempts_Hackathon_5_YearsOutput.csv', 'wb') as file1:
		fieldnames = ['Incident City', 'GEO', 'Case Number']
		writer = csv.DictWriter(file1, fieldnames = fieldnames)
		#writer.writeheader()
		for data in reader:
				g = geocoder.google(data['Incident Location']+", "+data[ 'Incident City']+', '+data['Incident State'])
				writer.writerow({'Incident City': g.latlng, 'Case Number' : data['Case Number']})
				print data[ 'Incident City']+', '+data['Incident State']
		file1.close()


