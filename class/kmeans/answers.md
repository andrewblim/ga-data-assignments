
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
- `probs.pkl` is a list of length k. The ith element of k is in turn a list containing 3-tuples (state-abbr, count, cluster-count), indicating the number of times count out of a possible cluster-count that an item in the ith cluster was found in region state-abbr. The list is sorted from most to least frequent. So for example x[0][0] might yield `('ca', 9371, 28249)`, indicating that in cluster 0 the region in which plants were most commonly found was California, 9371 times out of a possible 28249. Looking at the first 10 elements of each cluster is a nice quick way to get an idea of its contents. 

The script also prints the fraction of variance explained for each iteration of k. Here is a typical run:

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

You can generate heatmaps by adding the `--maps` flag when you run `run_kmeans.py`. These are per-cluster maps where US and Canadian states/provinces are shaded by the fraction of plants in the cluster that appear in that state/province. (No Greenland and Newfoundland/Labrador were skipped because the shapefiles I got treated them as one single province but the plant data separated them, it was just easier to skip.)

You need to have the basemap package, which in turn requires the GEOS library. Working on OS X, I was able to straightforwardly install GEOS with `brew install geos` but I did need to download and install basemap from source, pip didn't work for some reason. 

Using `--maps` can be slow and if you apply it to k-means for all k from 1 to 20, you'll be waiting a while for it to complete. (In particular the script has to reread the shapefiles for each image, which seems wasteful but I couldn't find an easy way around this.) I suggest you only try one or a few at a time. I also saved some of the images I generated myself on 4-means and 13-means into the `presaved_images` directory (corresponding to the two thresholds mentioned in hte previous section), if you want to look at them without regenerating them. 

Shapefiles were obtained from the NOAA: 

- [US](http://www.nws.noaa.gov/geodata/catalog/national/html/us_state.htm)
- [Canada](http://www.nws.noaa.gov/geodata/catalog/national/html/province.htm)

I'm also giving a shoutout to [this forum post](http://osdir.com/ml/python.matplotlib.general/2005-09/msg00205.html) which helped me learn how to use basemap (I didn't know how to draw nice data visualization maps, and this was a nice help in getting started). 

### What clustering does for us

Here k-means clustering provides a natural way to group plants into biomes, one that is especially made clear with the map visualizations. Each cluster represents a group of plants that tend to be found in the same geographic regions, and the clusters reveal where the main boundaries between plant biomes lie. 

In the 4-means example in `presaved_images`, we have clusters that represent the Southeast, the West/Northwest, "everywhere" (plants that are found all over North America), and "nowhere" (a catch-all bucket it seems, it's far bigger than the other clusters, there is some favoritism towards the Southwest but no state appears too frequently). The non-representation of the Northeast in its own cluster means that Northeast plants fell into the "everywhere" bucket, which in turn suggests that Northeast plants are more similar to general plant life nationwide than any other region. In fact in the "everywhere" map the Northeast is shaded a bit more darkly. 

In the 13-means example you get finer detail. For example there is one cluster that appears to focus on California, one focused on Puerto Rico, and the Northeast has a cluster to itself now. The one that on casual glance appears to be blank is actually a large, weakly similar group in which Hawaii is the most frequently found region. 

Note that the coloration is done based on probability, _fraction_ of plants in each cluster. If you have a small cluster you may get some very dark shadings even though the absolute number of plants matching that profile is small. 

There is a labeling error in the data here which I've left unfixed as an interesting example of what else clustering can do. In the maps you'll see that Alabama and Alberta often appear reversed from what they should be. This is particularly clear in the 4-means example. I'd assumed I'd messed up at first, but the state abbreviations file does indicate Alabama as "ab" and Alberta as "al", which I think is almost certainly backwards. There are some other pieces of evidence to support this: they are backwards going by postal abbreviation, and in the raw data each plant generally lists US regions first and Canadian regions second, and "ab" is found with the Canadian regions. But I would not have found this if not for the visualization of the clustering. 

## pip freeze

    Jinja2==2.6
    PyYAML==3.10
    Pygments==1.5
    Sphinx==1.1.3
    basemap==1.0.5
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