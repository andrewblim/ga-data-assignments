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
                    transform_x=log,
                    summary_filename='fed_employment.summary.txt',
                    plot_filename='fed_employment.png')