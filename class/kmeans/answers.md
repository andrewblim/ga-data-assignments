
# K-means

Andrew Lim / 14 Nov 2012

### Answers

The data set I used was UCI's [Plants](http://archive.ics.uci.edu/ml/datasets/Plants). This contains two files: one mapping state/province abbreviations to names and one mapping plant species to a list of region abbreviations indicating where they can be found. There was very minor manual data cleanup required to get these into nice CSV format. The cleaned-up files are in `plants/plants.csv` and `plants/stateabbr.csv`. 

You can run the script as follows: 

- `python run_kmeans.py x y` will run k-means for k = x to k = y, inclusive. 
- `python run_kmeans.py x` will run k-means for k = x only. 
- `python run_kmeans.py` will run k-means from k = 1 to k = 5. 

For each k, the script will generate a directory called `<k>-means` containing two pickle files: 

- `model.pkl` is the sklearn KMeans() fitted model object. 
- `probs.pkl` is a list of length k. The ith element of k is in turn a list containing 2-tuples (state-abbr, probability), indicating the probability that an item in the ith cluster was found in region state-abbr, and sorted from most probable to least probable. So for example x[0][0] might yield `('ca', 0.2967085387183972)`, indicating that in cluster 0 the region in which plants were most likely to be found was California, with a probability of about 29.7%. Looking at the first 10 elements of each cluster is a nice quick way to get an idea of its contents. 

The script also prints the fraction of variance explained for each iteration of k. 

 - 1-means: 0.0000
 - 2-means: 0.3194
 - 3-means: 0.3799
 - 4-means: 0.4350
 - 5-means: 0.4722
 - 6-means: 0.4971
 - 7-means: 0.5216
 - 8-means: 0.5403
 - 9-means: 0.5531
 - 10-means: 0.5644
 - 11-means: 0.5785
 - 12-means: 0.5884
 - 13-means: 0.5995
 - 14-means: 0.6082
 - 15-means: 0.6154

As a check, k = 1 does output 0. You can run this over a wide range of values of k as I did to get an idea of what an appropriate number for k is. See [this Wikipedia article](http://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set]); this gave me the idea to plot variance explained against k. The marginal benefit to increasing k decreases steadily, so we can impose some kind of minimum benefit threshold like 0.05 (in which case we'd stop at k = 4) or 0.01 (in which case we'd stop at k = 13). 

### Visualizations

You can generate these by adding the `--maps` flag when you run `run_kmeans.py`. You need to have the basemap package, which in turn requires the GEOS library. Working on OS X, I was able to straightforwardly install GEOS with `brew install geos` but I did need to download and install basemap from source, pip didn't work for some reason. 

Using `--maps` can be slow and if you apply it to k-means for all k from 1 to 20, you'll be waiting a while for it to complete. I suggest you only try one or a few at a time. I also saved some of the images I generated myself on 4-means and 13-means into the `presaved_images` directory, if you want to look at them without rerunning the script. 

Shapefiles were obtained from the NOAA: 

- [US](http://www.nws.noaa.gov/geodata/catalog/national/html/us_state.htm)
- [Canada](http://www.nws.noaa.gov/geodata/catalog/national/html/province.htm)

I'm also giving a shoutout to [this forum post](http://osdir.com/ml/python.matplotlib.general/2005-09/msg00205.html) which helped me learn how to use basemap (I didn't know how to draw nice maps, and took this as an opportunity to learn). 
