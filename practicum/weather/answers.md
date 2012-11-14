
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

We discussed this a bit in the last class assignment, but: there are two major differences. 

One is that Dark Sky will not always pick the three nearest neighbors. Dark Sky creates a triangulation based on the station data and each point is computed based on its bounding triangle. You can construct a set of points where the vertices of the bounding triangle are not the same as the nearest neighbors; for example if you have three points ABC in a small triangle and a fourth point D very far away, you'll have points in some triangle ABD that are actually closest to A, B, and C. 

The other is the method by which the neighbor data are aggregated. We are just averaging the temperature for the neighbors (the default weighting for KNeighborsRegressor in sklearn). Dark Sky weights inversely proportional to a point's distance from each neighbor: it weights neighbor by barycentric coordinate, which is the weight each neighbor would have to bear in order for the point in question to be the center of mass of the neighbors' weights. sklearn has an inverse weighting option but it weights proportionally to the inverse of the distance from each coordinate, which is not quite the same thing: a point on the edge of a bounding triangle (assuming the vertices also happen to be the nearest neighbors) would have 0 barycentric weight to the opposite vertex but would have nonzero weight with inverse distance weighting. 

### Problem 8

A regression on (latitude, longitude) will be of the form y = b0 + b1 * x1 + b2 * x2, which is the equation of a plane. So a linear regression fit on the same data will look like a plane - it'll be tilted in some direction broadly corresponding to what minimized the squared error, but there will be no bumps, hills, or other convexities in the surface of the fit. Looking at the images, many of the warmer points are on the East Coast and many cooler points are in the Midwest, so the plane will probably be tilted towards higher temperatures East - consequently it'll probably get all of the West Coast wrong because it has no way to curve the temperature back up. 

### Problem 9

One way to judge the efficacy of the two models is to cross-validate. To run this, run `python run_weather.py xv`. This will randomly split the data for the first hour of data into five equal-sized folds, train 5-NN and linear regression on four out of the five folds, and predict temperature for the last fold. It returns the root mean squared error for both approaches. 

The exact values will differ by run, but I got RMSEs of around 3-4 for 5-NN and 7-8 for linear regression when I ran it right before submission. 

### Problem 10

The haversine formula for distance along a sphere's (the Earth's) surface is: 

h(d/r) = h(lat2 - lat1) + cos(lat1) * cos(lat2) * h(lon2 - lon1)

When we applied Euclidean distance to latitude and longitude, the following distortions in h(d/r) occurred: 

- East-west distances were overstated relative to north-south distances. A 1 degree change in latitude is a larger move than a 1 degree change in longitude everywhere except at the equator, since when changing latitudes you're always moving along a great circle, but when changing longitudes you're on a small circle everywhere but at the equator. This can be seen in the formula: cos(lat1) * cos(lat2) is never greater than 1, so moving 1 degree lon impacts h(d/r) less than 1 degree lat, all else held equal. Therefore when using Euclidean distance we overstated the geographic distance between stations along the east-west axis. 

- East-west distances at higher latitudes were overstated relative to east-west moves nearer the equator. At high latitudes, 1 degree longitude is a much smaller distance at the equator. This can be seen by the fact that when lon2 - lon1 = 1 and lat1 = lat2 (i.e. we're not changing latitudes), h(d/r) is maximized when lat1 = lat2 = 0 (equator) and minimized (equaling 0) when lat1 = lat2 = pi/2 or -pi/2 (the poles). 

This shouldn't affect the kNN model too badly. For many points, especially in densely stationed areas where the distortions are over small distances and are small, the neighbors will be the same and the prediction will not change. In general when using great circle distance we should see predicted points being influenced more heavily by stations to the east and west, and increasingly so as we move to higher latitudes. 

### pip freeze

For reference, in case there are problems getting the code to run. 

    Jinja2==2.6
    PyYAML==3.10
    Pygments==1.5
    Sphinx==1.1.3
    beautifulsoup4==4.1.3
    boto==2.6.0
    distribute==0.6.28
    docutils==0.9.1
    ipython==0.13.1
    matplotlib==1.1.1
    mrjob==0.3.5
    nose==1.2.1
    numpy==1.6.2
    pandas==0.9.0
    patsy==0.1.0
    python-dateutil==2.1
    pytz==2012h
    pyzmq==2.2.0.1
    rpy2==2.3.0beta1
    scikit-learn==0.12.1
    scipy==0.11.0
    simplejson==2.6.2
    six==1.2.0
    statsmodels==0.5.0
    tornado==2.4
    wsgiref==0.1.2