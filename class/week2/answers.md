
# Data Class Week 2 Answers

Andrew Lim / 17 Oct 2012

I used Google Refine to clean up my data and get it in the format I wanted, so all the csv files supplied with this problem set are already in a nice format. Great utility! On the other hand, I couldn't get regressionplots from statsmodels to work properly without a cryptic KeyError (seems to be related to drawing the confidence bands, as I get the graph without the bands to appear before the exception gets thrown). So I just made the plots with matplotlib directly, unfortunately I'm missing confidence bands. All regressions include an intercept term. 

To run everything, run `python run_regressions.py`. 

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

### Problems

#### log(GDP per capita) vs. life expectancy at birth

GDP is in constant 2005 dollars, life expectancy is in years. I used data from the [World Bank](http://data.worldbank.org/) for all country-year combinations from 2002 to 2011, throwing out any entries that didn't have both a GDP per capita and life expectancy figure. 

The R^2 is 0.637. 

- Data (input): `worldbank_lifeexp_gdp.csv`. 
- Results (output): `worldbank_lifeexp_gdp.summary.txt`
- Plot (output): `worldbank_lifeexp_gdp.png`

#### Change in unemployment rate vs. change in labor force participation rate

I didn't have any particular expectations about this but the issue of participation rates making the unemployment statistics look better than they "really" are has been a subject of recent political conversation. If I had to guess, I would have said that changes in the two rates were negatively correlated, since I think poor economic prospects lead to people dropping out of the labor force entirely, and vice versa for good economic prospects. I used data from the [St. Louis Fed](http://research.stlouisfed.org/fred2/), with data going all the way back to 1948. 

The R^2 is 0.022, really basically 0. 

- Data (input): `fed_employment.csv`. 
- Results (output): `fed_employment.summary.txt`
- Plot (output): `fed_employment.png`

#### NYC (large) high school 2010 SAT math scores vs. writing scores

Data came from [NYC OpenData](https://nycopendata.socrata.com/Education/SAT-College-Board-2010-School-Level-Results/zt9s-n5aj). I would expect a positive correlation, as I'm pretty sure the main axis of variation amongst high schools' test-taking scores is good scores and bad scores, not strong in math vs. strong in writing. I eliminated any schools with fewer than 50 reported scores, which still leaves plenty of data (> 200 lines). I tried to predict math scores from writing scores. 

The R^2 is high as expected, 0.852. The interesting outlier on the fit has one of the poorest writing scores, at 314, but a well above-average math score at 532 (mean 435, median 419, standard deviation 71.5). This school is the Lower East Side Preparatory High School and it's in Chinatown, and judging by its [website](http://www.lespnyc.com/) it seems to serve a heavily Chinese student body. 

- Data (input): `nycdata_satbyschool.csv`. 
- Results (output): `nycdata_satbyschool.summary.txt`
- Plot (output): `nycdata_satbyschool.png`

#### Property crime rate and poverty rate by state

Data came from the US Census and is from 2009: [here](http://www.census.gov/compendia/statab/cats/law_enforcement_courts_prisons/crimes_and_crime_rates.html) for crime and [here](http://www.census.gov/compendia/statab/cats/income_expenditures_poverty_wealth/income_and_poverty--state_and_local_data.html) for poverty. Property crime is per 100k people, so it's normalized for different state populations. I'd expect a weakly positive correlation, as crime and poor economic straits often go hand in hand, and the desperately poor may be driven to property crime - however I don't think it'll be too strong of a relationship in terms of how much variance is explained. I tried to predict crime rates from poverty rates. 

The R^2 is 0.289. 

- Data (input): `census_crime_poverty.csv`. 
- Results (output): `census_crime_poverty.summary.txt`
- Plot (output): `census_crime_poverty.png`

