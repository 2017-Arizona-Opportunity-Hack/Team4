# Team4

Opportunity Hack 2017
National Center for Missing and Exploited Children

#### Notes:

Time column in "attempted" has been reformatted to "hhmm" in Excel. This allows
us to filter by times and build charts more easily.

Date column in "attempted" and "missing" has been reformatted to "yyyy-mm-dd" 
in Excel. This allows us to filter out instances based on dates more easily.

Added the columns "Lat", "Lon" for latitude and longitude of incidents in
"attempted" and "missing", which allows us to show incidents that occur within
a square of a given size (easier than searching for incidents in a circle).

The Google Maps API allows you to make free requests up to a certain amount,
but after that it requires a special user key and charges for access. Up to
25,000 map loads per day, and $0.05 for every additional map load.

#### Requirements:

* Python 2.7
* Internet connection for Google Maps API requests
* Various libraries listed in `requirements.txt`

#### Running:

1. Open command prompt, cd to the directory containing the project

`cd \path\to\project`

2. To run the project, type in

`python main.py`

3. Assuming that all of the libraries are up and running correctly, a window
should show up with a map in it.

4. From here you can choose to load an existing CSV file and apply the filters
on the left-hand side of the window. Note that the CSV files that you load
**must** have the following columns in them:

**Missing**
 * Gender
 * Missing State
 * Age Missing
 * Missing Date
 * Lat
 * Lon
 
**Attempts**
 * Child Gender [1, 2, 3, 4, 5, 6]
 * Child Perceived Age [1, 2, 3, 4, 5, 6]
 * Incident State
 * Incident Date
 * Offender Method [Animal, Candy, Money, Ride, Other]
 * Lat
 * Lon
 
These columns are used in the filtering process. One of our biggest challenges
was converting addresses into latitude/longitude values. There are a plethora
of free services available, our issue was over-taxing the free system past our
daily limits.
