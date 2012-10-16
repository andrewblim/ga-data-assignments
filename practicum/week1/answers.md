
# Practicum Week 1 Answers

Andrew Lim
14 Oct 2012

To run everything, run `python mtafare.py all`, or run a problem individually with `python mtafare.py [number]` (can be 2-5 or 7-9). 

`pip freeze` on my virtualenv: 

    Pygments==1.5
    ipython==0.13
    matplotlib==1.1.1
    nose==1.2.1
    numpy==1.6.2
    pandas==0.9.0
    patsy==0.1.0
    python-dateutil==2.1
    pytz==2012f
    pyzmq==2.2.0.1
    scikit-learn==0.12.1
    scipy==0.11.0
    six==1.2.0
    statsmodels==0.5.0
    tornado==2.4
    wsgiref==0.1.2

### Problem 1

The data set I used was from [Saturday 6 Oct 2012](http://mta.info/developers/data/nyct/fares/fares_121006.csv), not the latest by now, but it was when I started. 

### Problem 2

Info is printed to `dictionary_dump.txt`.

### Problem 3

The histogram is output to `problem3.png`. 

The max value, the outlier, is 246521. The mean value is 7089.1602. The median value is 257. The mean is greater than the median. This makes sense because the distribution is positively skewed - there is an upper tail of values that are very large compared to most of the values in the data. These will pull the mean upwards, but not the median, as extremely large and slightly large values are offset equally by small values in its calculation. 

The outlier is remote R170, 14th St./Union Square. 

### Problem 4

The histogram of PATH 2-trip swipes is output to `problem4_path.png`. The vast majority of entries are 0 and just a few (14) are nonzero but sometimes much higher (the max is 8794). It corresponds to the fact that you'd only ever use a PATH 2-trip card at the small handful of PATH stations. 

The histogram of students is output to `problem4_students.png`. It's "interesting" in some sense because there are no swipes whatsoever. It's zero across the board. I'd need more detail on what exactly "STUDENT" means for sure, but I did Google it and discovered that there is some kind of card that is very limited, both in # of swipes and usable time frame. If this is it, then barring any error in the data, the student program is highly underused; either it's a really poor deal for families, or it's really under-publicized, or the few students that use it don't use the subways (works on buses as well). 

### Problem 5

The plot is output to `problem5.png`. 

The two are positively correlated with each other. Both feature an upside tail, as most values are clustered in the lower left of the plot and a few scattered values are to the upper right. There are a number of points with 0 values for 30-day unlimited swipes, suggesting that there may be some stations where no one ever swipes in with an unlimited pass (guess: perhaps those particular stations do not accept them). 

### Problem 6

I used data up to and including [Saturday 6 Oct 2012](http://mta.info/developers/data/nyct/fares/fares_121006.csv), so not the newest posting that got put up after I started working on this. I manually chopped off one item, the entry posted [Thursday 13 Jan 2011](http://mta.info/developers/data/nyct/fares/fares_110113.csv), the only non-Saturday entry in the data. Based on the file description this seems redundant. The file's headers describe a date span that matches the date span from [Saturday 8 Jan 2011](http://mta.info/developers/data/nyct/fares/fares_110108.csv), but the values are slightly different - I've elected to chop the Thursday one. 

### Problem 7

The data is output to `transformed_data.csv`. I'm aggregating all swipe counts regardless of type. 

### Problem 8

Although done within Python, the sort is achieved by executing a Unix command: `awk 'NR == 1 { print } NR > 1 { print | "sort" }' transformed_data.csv > sorted_data.csv`. The sorted data is output to `sorted_data.csv`. The grouped data is output to `grouped_data.csv`. 

Caveats on the grouping: 

- We are grouping by station ID, not by remote - multiple remotes are in some cases associated with the same station name (example: "25TH STREET-4TH AVENUE" is associated with remotes R278 and R455). I believe in general these correspond to different swipe locations at the same stop so I'm just aggregating them by date, although I'm not positive that there isn't a pair of identically named stations somewhere representing different physical stops. 

- There are many entries that are not present in every available week (121 possible weeks). There are some that are there for only part of the time and are missing at other times (example: "AQUEDUCT RACE TRACK"). There are a few that I suspect aren't real remotes and don't belong in the data set (example: "METROCARD VAN 1"), but I'm not going to remove them as I don't know enough to say they should be thrown out for sure. And of course there are spelling changes and typos, fun. "241ST ST-WHITE PLAINS RD" vs. "241TH ST-WHITE PLAINS RD", "KOSCIUSKO STREET-BROADWAY" vs. "KOSCIUSZKO STREET-BROADWAY", etc. All this is to say that the station names would have to be cleaned up to get the data really proper, which I haven't done. 

- That having been said, any station missing data on a given week gets it marked as blank (not zero; the average is only taken over available weeks). 

### Problem 9

I'll look at [Saturday 6 Oct 2012](http://mta.info/developers/data/nyct/fares/fares_121006.csv) as in the early problems, to make life easy. "Below" median also includes median itself for all buckets. 

Below median on both: 202
Below median on 30-D UNL, above on FF: 29
Above median on 30-D UNL, below on FF: 29
Above median on both: 202

The probability of a remote being above median on full fare given that it's above median on 30-day unlimited is 202/(202+29), or 87.4%. 

### Problem 10

I actually think there's not enough to answer this one (assuming it's a probability question and you don't want us to find out what proportion of stations are in Manhattan)? We are given that Pr(Manhattan | high) is 0.3. Pr(high) and Pr(low) are 0.5 by definition of median. That means: 

Pr(Manhattan and high) = 0.5 * 0.3 = 0.15
Pr(not Manhattan and high) = 0.5 - 0.15 = 0.35

But we don't know anything about Pr(Manhattan and low) and Pr(not Manhattan and low), except that they sum to 0.5. They could be 0.5 and 0 respectively, in which case Pr(high | Manhattan) would be 0.15 / 0.65 = 23%, or they could be 0 and 0.5 respectively, in which case Pr(high | Manhattan) would be 100%. 