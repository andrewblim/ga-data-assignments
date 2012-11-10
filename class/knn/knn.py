import matplotlib.figure as figure
import matplotlib.pyplot as pyplot
import numpy as np
import os
import os.path
import pandas as pd
import pickle
import sklearn
import statsmodels.api as sm
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier

def generate_histograms(input_filename, output_dir, sep=';', **kwargs):
    '''Generate histograms of the data in csv file input_filename to directory
    output_dir. kwargs are passed to matplotlib.pyplot.hist(). 
    '''
    x = pd.read_csv(input_filename, sep=sep)
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
    for col in x.columns:
        pyplot.title(col)
        pyplot.hist(x[col], **kwargs)
        pyplot.savefig(os.path.join(output_dir, '%s.png' % col))
        pyplot.close()

def read_csv_response_predictors(filename, sep=';', y_col='quality', cols=None, transforms=None):
    '''Read the csv file at filename with a column y_col indicated as the 
    response variable and optionally a list cols of predictor variables to use
    (default is to use all other columns). Optionally apply a function to each
    as indicated by the dict transforms { colname : function }. Returns tuple
    (response data, predictor data). 
    '''
    x = pd.read_csv(filename, sep=sep)
    if cols is not None:
        x = x[cols + [y_col]]
    if transforms is not None:
        for (col, transform) in transforms.items():
            if col in x.columns:
                x[col] = transform(x[col])
                x.rename(columns={col: '%s(%s)' % (transform.__name__, col)}, 
                         inplace=True)
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

def run_all_predictors(input_filename, output_dir, response, predictors=None, 
                       transforms=None, 
                       models={'lr': lambda y, x: linear_regression(y, x, constant=True)},
                       predict_override={'lr': lambda p, x: getattr(p, 'predict')(sm.add_constant(x, prepend=True))}):
    
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
    
    print('Reading data...')
    (y, x) = read_csv_response_predictors(input_filename, 
                                          y_col=response,
                                          cols=predictors,
                                          transforms=transforms)
    
    if predictors is None:
        print('Predicting %s on all other variables...' % response)
    else:
        print('Predicting %s on %s...' % (response, predictors))
    
    print('Fitting models and generating predictions...')
    fitted_models = {}
    predictions = pd.DataFrame({'actual': y})
    for model_name in models:
        fitted_models[model_name] = models[model_name](y, x)
        if model_name in predict_override:
            predictions[model_name] = predict_override[model_name](fitted_models[model_name], x)
        else:
            predictions[model_name] = fitted_models[model_name].predict(x)
    
    print('Writing out files...')
    predictions.to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)
    for model_name in fitted_models:
        if 'summary' in dir(fitted_models[model_name]):
            f = open(os.path.join(output_dir, '%s_summary.txt' % model_name), 'w')
            f.write(fitted_models[model_name].summary().__str__() + '\n')
            f.close()
        pickle.dump(fitted_models[model_name], 
                    open(os.path.join(output_dir, '%s_model.pkl' % model_name), 'wb'))
    
    print('RMSEs:')
    for model_name in sorted(models.keys()):
        mse = ((y - predictions[model_name])**2).mean()**0.5
        print('%s: %.4f' % (model_name, mse))
        