from pylab import *
import pandas as pd
import statsmodels.api as sm
import sys

def simple_regression(data_filename, col_x, col_y, transform_x=None, 
                      transform_y=None, summary_filename=None, 
                      plot_filename=None):
    data = pd.read_csv(data_filename)
    if transform_x is None: 
        x = data[col_x]
    else: 
        x = pd.Series(transform_x(data[col_x]), 
                      name='%s(%s)' % (transform_x.__name__, col_x))
    if transform_y is None: 
        y = data[col_y]
    else: 
        y = transform_y(data[col_y])
        y = pd.Series(transform_y(data[col_y]), 
                      name='%s(%s)' % (transform_y.__name__, col_y))
    X = sm.add_constant(x, prepend=True)
    model = sm.OLS(y, X)
    results = model.fit()
    if summary_filename is None:
        print(results.summary())
    else:
        f = open(summary_filename, 'w')
        f.write(results.summary().__str__() + '\n')
        f.close()
    if plot_filename is not None:
        scatter(x, y)
        grid(b=True, which='major', color='#505050')
        xlabel(x.name)
        ylabel(y.name)
        line_x = [min(x), max(x)]
        line_y = [results.predict([1,a]) for a in line_x]
        plot(line_x, line_y, color='r')
        savefig(plot_filename)
        close()
    return (data, results)