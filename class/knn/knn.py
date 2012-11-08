import numpy as np
import pandas as pd
import sklearn
import statsmodels.api as sm
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier

def read_wine_csv(filename, sep=';', y_col='quality', transforms=None):
    x = pd.read_csv(filename, sep=sep)
    if transforms is not None:
        for (col, transform) in transforms.items():
            x[col] = transform(x[col])
        x.rename(columns={col: 'log1p(%s)' % col for col in transforms}, inplace=True)
    y = x.pop(y_col)
    return (y, x)    

def linear_regression(y, x, cols=None, constant=True, constant_prepend=True):
    if cols is not None:
        x = x[cols]
    if constant: x = sm.add_constant(x, prepend=constant_prepend)
    return sm.OLS(y, x).fit()

def nearest_neighbors_regressor(y, x, cols=None, **kwargs):
    if cols is not None:
        x = x[cols]
    return KNeighborsRegressor(**kwargs).fit(x, y)

def nearest_neighbors_classifier(y, x, cols=None, **kwargs):
    if cols is not None:
        x = x[cols]
    return KNeighborsClassifier(**kwargs).fit(x, y)