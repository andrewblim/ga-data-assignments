from pylab import *
from regressions import simple_regression

if __name__ == '__main__':
    
    print('Regressing life expectancy on GDP per capita')
    simple_regression(data_filename='worldbank_lifeexp_gdp.csv', 
                      col_x='GDP/capita, PPP (2005 $)',
                      col_y='Life exp. at birth (yrs)',
                      transform_x=log,
                      summary_filename='worldbank_lifeexp_gdp.summary.txt',
                      plot_filename='worldbank_lifeexp_gdp.png')
    
    print('Regressing change in unemployment rate on change in participation rate')
    simple_regression(data_filename='fed_employment.csv', 
                    col_x='Civilian participation (% change)',
                    col_y='Unemployment rate (% change)',
                    summary_filename='fed_employment.summary.txt',
                    plot_filename='fed_employment.png')
    
    print('Regressing SAT math scores on SAT writing scores')
    simple_regression(data_filename='nycdata_satbyschool.csv', 
                      col_x='Writing Mean',
                      col_y='Mathematics Mean',
                      summary_filename='nycdata_satbyschool.summary.txt',
                      plot_filename='nycdata_satbyschool.png')
    
    print('Regressing crime by state on poverty rate by state')
    simple_regression(data_filename='census_crime_poverty.csv', 
                    col_x='Poverty rate',
                    col_y='Property crime (per 100k)',
                    summary_filename='census_crime_poverty.summary.txt',
                    plot_filename='census_crime_poverty.png')

    print('Regressing NBA points per game on percentage of points from 3s')
    simple_regression(data_filename='nba_seasons.csv', 
                    col_x='Pct points from 3s',
                    col_y='Points per game',
                    summary_filename='nba_seasons.summary.txt',
                    plot_filename='nba_seasons.png')