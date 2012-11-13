
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

`python run_weather.py csv` generates the data to `temperature.csv`. There is one misplaced station in the data which I've manually corrected - the West Memphis, AR station should have a longitude of 90.23W. 

### Problem 3

`python run_weather.py colorplot` generates a set of pngs to directory `colorplot`, one for each hour. 

### Problems 4-6

`python run_weather.py knn` generates a set of pngs to directories `grid_1nn`, `grid_2nn`, and `grid_5nn`, one for each hour, run with kNN on 1, 2, and 5 nearest neighbors, respectively. This graph is zoomed in on the NYC area. The diamond scatterpoints laid over the grid indicate where the actual NOAA stations are. With fewer neighbors the predicted temperature changes more discontinuously as you move around geographically; on 1-NN you can see clearly delineated regions around some of the stations. As you increase k the predictions become smoother. 

You can also clearly see the coastline in these graphs. The predictions made out over open water are probably unreliable since kNN is forced to use distant stations to predict temperature; this is akin to a regression being extrapolated way beyond the domain of the data on which it was trained. 

### Problem 7

### Problem 8

`python run_weather.py silly`

### Problem 9

### Problem 10

### pip freeze

