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
		return 1
	elif len(myList) == 62 and myList[0] =="Case Type":
		return 0
	else:
		return -1