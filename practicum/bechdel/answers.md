# Bechdel Test

Andrew Lim / 27 Nov 2012

### To run everything

Run `python run_bechdel.py`. 

If you've already run this and want to run it again without re-parsing the Bechdel page and re-running the OMDB queries, run `python run_bechdel.py --no-data`, which will assume you already have a file `bechdel_full.csv` to use. 

### Problems 1-3

Run `python run_bechdel.py --data` to dump the raw data into `bechdel_full.csv`. All data from the OMDB interface as well as the Bechdel rating categories `{few_women, no_talk, men_talk, pass}` are included, with no refinement at this stage. 

This step comes with the usual caveats that the source data isn't perfect. There are a handful of duped titles that will throw warnings to stdout, and in two cases the duped titles actually have different ratings! (See "2046", right at the top of the page.) Also, there are some clear errors; "The Joy Luck Club" apparently fails the test because it doesn't have two named women in it. Really? The Joy Luck Club? 

### Problem 4

Run ``

The parental advisory rating is a little tricky because about 1/3 of the entries are not one of the MPAA standards {G, PG, PG-13, R, NC-17}. See this list of [motion picture rating systems by country](http://en.wikipedia.org/wiki/Motion_picture_rating_system). I bucketed the ratings into MPAA equivalents and shoehorned the other ratings into a bucket, with a few indeterminate ratings not given any bucket (particularly unhelpful is the fact that different countries use the same letter for different severities). These aren't trivial but are not a large percentage of the data. 

- "general": G, 6, 7, Atp, K-3, TV-G
- "guidance": PG, M, 9, 10, 11, K-8, K-11, TV-PG, Y7
- "teen": PG-13, 12, 12A, 13, 13+, 14, 14A, 15, 15A, K-12, K-13, K-15, M/12, MA15+, PG-12, R-12, TV-14, VM14
- "mature": R, NC-17, 16, 18A, K-16, M/16, M18, NC-16, R18, TV-MA, VM18, X
- "pre_mpaa": Approved, Passed
- "unrated": N/A, Not Rated, Unrated
- not bucketed: A, AL, AII, C, E, GP, I, II, IIB, L, MA, S, T

A few notes: the "Approved" and "Passed" movies appear to be old films that were subject to binary approval/disapproval for release before the current MPAA system was put in place. They are about 8% of the films so I thought they deserved their own category separate from "unrated". The unbucketed films are a little over 1%. 

https://www.census.gov/genealogy/www/data/1990surnames/dist.female.first


### pip freeze