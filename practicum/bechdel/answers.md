# Bechdel Test

Andrew Lim / 5 Dec 2012

### To run everything

Run `python run_bechdel.py`. 

If you've already run this and want to run it again without re-parsing the Bechdel page and re-running the OMDB queries, run `python run_bechdel.py --all-but-data`, which will assume you already have a file `bechdel_full.csv` to use. I also included a `bechdel_full.csv` in here which should work for this purpose, just in case the Bechdel website changes and breaks my code by the time you look at it. 

### Problems 1-3

Run `python run_bechdel.py --data` to dump the raw data into `bechdel_full.csv`. All data from the OMDB interface as well as the Bechdel rating categories `{few_women, no_talk, men_talk, pass}` are included, with no refinement at this stage. This step can take a little while. 

There are a handful of duped titles that will throw warnings to stdout, and in two cases the duped titles actually have different ratings. (See "2046", right at the top of the page.) I use the first one in these instances. Also, there are some clear errors; "The Joy Luck Club" apparently fails the test because it doesn't have two named women in it. Really? The Joy Luck Club? 

### Problem 4

Run `python run_bechdel.py --features` to construct a csv file `features.csv`. The features are:

- year, IMDB rating, count of IMDB votes
- indicators for each month
- indicators for each parental rating category (further explanation below)
- indicators for each IMDB genre
- runtime in minutes and an indicator for entries without available runtime data
- indicator for presence of one or more "female words" (further explanation below)
- indicator for zero or one female names in the actress list (further explanation below)

#### Ratings

Although the majority of the ratings are MPAA standard G, PG, etc., about 1/3 are not, in most cases a rating from another country's parental guidance system. See this list of [motion picture rating systems by country](http://en.wikipedia.org/wiki/Motion_picture_rating_system). I bucketed the ratings as indicated below and shoehorned everything into one of them. 

- "general": G, 6, 7, Atp, K-3, TV-G
- "guidance": PG, M, 9, 10, 11, K-8, K-11, TV-PG, Y7
- "teen": PG-13, 12, 12A, 13, 13+, 14, 14A, 15, 15A, K-12, K-13, K-15, M/12, MA15+, PG-12, R-12, TV-14, VM14
- "mature": R, NC-17, 16, 18A, K-16, M/16, M18, NC-16, R18, TV-MA, VM18, X
- "pre_mpaa": Approved, Passed
- "unrated": N/A, Not Rated, Unrated
- not bucketed: A, AL, AII, C, E, GP, I, II, IIB, L, MA, S, T

The "Approved" and "Passed" movies appear to be old films that were subject to binary approval/disapproval for release before the current MPAA system was put in place. They are about 8% of the films so I thought they deserved their own category, separate from "unrated". The unbucketed ratings are a small percentage of the data, a little over 1%. 

#### Female words

I included an indicator variable indicating whether or not the plot synopsis contained "female words" like "she", "her", "woman", "daughter", etc. I used [Vivake Gupta's implementation of the Porter Stemmer algorithm](http://tartarus.org/martin/PorterStemmer/python.txt) (no license attached to the code) to stem the plot into manageable stems. The file `female_words.txt` contains a list of "female" words I picked by hand whose stems' presences are checked in the plot synopses. 

#### Female names

I included an indicator variable indicating the number of female names found amongst the actors. The female names are in `female_firstnames.txt` and are based off the top 500 entries in a list of the most popular female names in the US as of the 1990 census (1990 was just the first thing I found and should work fine). The file can be obtained [here](https://www.census.gov/genealogy/www/data/1990surnames/dist.female.first). I set the cutoff at 500 names somewhat arbitrarily, mainly to prevent bad false positives from mucking up the feature. Would you believe that the name "Michael" comes in at #799 and "John" is at #819? "Johnnie" is at #391 and I've decided just to live with that one. And of course there are some names that can go either way that will make this variable less effective than otherwise (sorry, Leslie Nielsen), but I suppose given names alone there's not a lot I can do short of a really long hand-check. 

### Problems 5-6

Run `python run_bechdel.py --prediction` to run prediction and analysis based on the data in `features.csv`. This runs a logistic regression with a constant term included. 

Output files: 

- `genre_corr.png`
- `roc.png`
- `precision_recall.png`
- `bootstrap.txt`

First `features.csv` is read in and an image `genre_corr.png` is generated showing the correlations between the different genre labels. This is more of a sanity check to see whether any of the genres overlap too much (they don't - the closest thing to a problem is that "Animation" and "Family" have a corr in the 0.50s). 

Then a single run of 10 cross-validation folds is used to generate predictions. These will in turn generate an ROC graph, which is output to `roc.png`, and a precision-recall graph, which is output to `precision_recall.png`. The AUCs I've seen on the ROC curve have fallen in the 0.69 - 0.75 range, with an average of 0.72. 

Finally 100 logistic regressions are run, each with 10 randomized folds, so that 1000 values for each coefficient are generated. The program then outputs the 95% confidence intervals and the coefficients that were significant at the 95% threshold to `bootstrap.txt`. 

I was pleased to see that among the indicator features, the ones I added were among the strongest in terms of magnitude, indicating significant impact on the probability that a film is Bechdel pass. They were in the expected direction. `Female_word` was easily the largest coefficient, around 0.68 on average in the bootstrap, indicating that female words in the plot synopsis strongly increase the likelihood that a film is Bechdel pass. `Actress_0` and `Actress_1` were negative, about -0.33 and -0.18 respectively, indicating that the presence of 0 or 1 female names only in the actors list (as opposed to 2+ female names) made Bechdel failure more likely. `Actress_0`, as expected, was larger in magnitude than `Actress_1`. 

Among genres, there were some non-surprises: action, adventure, crime, and war films are less likely to pass, drama is more likely. Interestingly horror is also more likely, I suppose you have women talking about how to run away from the killer rather than the men in their lives. Also interestingly but not entirely surprisingly, romance is not significantly different from 0. Among parental guidance ratings, adult and teen films are more likely to pass, and the pre-MPAA rated films were less likely, which was interesting; I guess older films failed the test more often (this is corroborated by a significant and positive coefficient on the year). 

### Problem 7

Run `python run_bechdel.py --reduced-prediction`. It reduces the features greatly, outputs them to `features_reduced.csv`, and then runs the same analysis over again. 

Rather than adding more features, I took away features to see how efficiently the model could still perform. At first I was going to chop everything but the coefficients that the bootstrap found to be significant. But I found that reducing it even further to just the lexical features I added produced a very comparable average ROC AUC, typicall worse only by about 0.005. There are only three predictive features in this prediction: `Actress_0`, `Actress_1`, and `Female_word`. I also use a constant term again. 

Output files (no genre corr matrix since no genres are used)

- `roc_reduced.png`
- `precision_recall_reduced.png`
- `bootstrap_reduced.txt`

### pip freeze