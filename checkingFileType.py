import csv
import pandas as pd
import geocoder
from collections import defaultdict

def readFILE(fileName):
	df = pd.read_csv(fileName)
	myList = list(df)
	print myList[0]
	print len(list(df))
	if len(myList) == 12 and myList[0] =="Case Number":
		print "Hackathon_Missing_Child_5_Years_of_Data.csv"
	elif len(myList) == 62 and myList[0] =="Case Type":
		print "Attempts_Hackathon_5_Years_of_Data.csv"
	else:
		print "this file is corrupt"