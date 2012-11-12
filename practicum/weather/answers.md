
# Practicum - Dark Sky

Andrew Lim / 10 Nov 2012

### To run all code at once

`python run_weather.py`. For details, see the answers to individual problems. 

### Problem 1

Dark Sky uses publicly available data from the NOAA's ground stations and, based on a triangulation drawn between those points, calculates the temperature for intermediate points based on a weighted average of the three stations forming the bounding triangle around that point. I'm not sure how they calculate temperature for points outside of the triangulation (which you'd get along a convex-shaped coast, for example). 

- [Page with full NOAA forecast for all stations](http://www.nws.noaa.gov/mdl/gfslamp/lavlamp.shtml)
- [Documentation of this format](http://www.nws.noaa.gov/mdl/gfslamp/docs/LAMP_description.shtml)
- [Latest list of all stations, with state, latitude, and longitude](http://www.nws.noaa.gov/mdl/gfslamp/docs/stations_info_07172012.shtml)

### Problem 2

`python run_weather.py csv`



### pip freeze

