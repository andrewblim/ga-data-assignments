
# Data Class Week 2 Answers

Andrew Lim / 17 Oct 2012

I used Google Refine to clean up my data and get it in the format I wanted, so all the csv files supplied with this problem set are already in a nice format. Great utility! On the other hand, I couldn't get regressionplots from statsmodels to work properly without a cryptic KeyError (seems to be related to drawing the confidence bands, as I get the graph without the bands to appear before the exception comes up). So I just made the plots with matplotlib directly, unfortunately I'm missing confidence bands. 

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

#### 

I used data from the [St. Louis Fed](http://research.stlouisfed.org/fred2/)