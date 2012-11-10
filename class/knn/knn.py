import matplotlib.figure as figure
import matplotlib.pyplot as pyplot
import numpy as np
import os
import os.path
import pandas as pd
import pickle
import sklearn
import statsmodels.api as sm
import warnings
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier

def generate_histograms(input_filename, output_dir, sep=',', **kwargs):
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

def read_csv_response_predictors(filename, sep=',', y_col='quality', cols=None, transforms=None):
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
                       transforms=None, sep=',', folds=5,
                       models={'lr': lambda y, x: linear_regression(y, x, constant=True)},
                       predict_override={'lr': lambda p, x: getattr(p, 'predict')(sm.add_constant(x, prepend=True))}):
    '''Runs a set of predictors on csv data in input_filename. 
    
    input_filename, output_dir: self-explanatory
    response: the response variable; should be a column header in 
              input_filename
    predictors: the columns to use as predictors, or None for all
    transforms: a dict mapping column headers to functions which are applied
                to those columns, e.g.: {'col': lambda x: x**2}
    folds: number of cross-validation folds to run
    models: a dictionary mapping semantic model names to functions that take
            arguments y, x and return fitted models
    predict_override: a function indicating how to predict - if not specified
                      it'll use model.predict() (you may want to override for
                      models that use a constant)
    
    Outputs to the output directory a predictions.csv file of actual and 
    predicted response variable values, several *.pkl files for the fitted
    model objects, and a summary .txt file if available. Outputs RMSEs to
    stdout. 
    '''
    
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
    
    print('Reading data...')
    (y, x) = read_csv_response_predictors(input_filename, 
                                          sep=sep,
                                          y_col=response,
                                          cols=predictors,
                                          transforms=transforms)
    
    if predictors is None:
        print('Predicting "%s" on all other variables...' % response)
    else:
        print('Predicting "%s" on %s...' % (response, predictors))
    
    print('Generating folds...')
    n = len(y)
    index = np.arange(n)
    np.random.shuffle(index)
    test_indices = []
    test_size = int(n / float(folds))
    for i in range(folds):
        if i == folds-1: test_indices.append(index[i*test_size:])
        else: test_indices.append(index[i*test_size : (i+1)*test_size])
    
    print('Fitting models and generating predictions...')
    fitted_models = {}
    predictions = pd.DataFrame({'actual': y})
    for model_name in sorted(models.keys()):
    
        # fit folds models
        fitted_models[model_name] = []
        for i in range(folds):
            fit_bool = [j not in test_indices[i] for j in range(n)]
            fitted_models[model_name].append(models[model_name](y[fit_bool], x[fit_bool]))
    
        # predictions are the average across the k-fold models
        cur_prediction = pd.Series(index=range(n))
        model = fitted_models[model_name][i]
        if model_name in predict_override:
            for i in range(folds):
                cur_prediction[test_indices[i]] = predict_override[model_name](model, x)
        else:
            for i in range(folds):
                cur_prediction[test_indices[i]] = model.predict(x)
        predictions[model_name] = cur_prediction
    
    print('Writing out files...')
    predictions.to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)
    for model_name in fitted_models:
        if 'summary' in dir(fitted_models[model_name]):
            f = open(os.path.join(output_dir, '%s_summary.txt' % model_name), 'w')
            f.write(fitted_models[model_name].summary().__str__() + '\n')
            f.close()
        for i in range(folds):
            pickle.dump(fitted_models[model_name], 
                        open(os.path.join(output_dir, '%s%d_model.pkl' % (model_name, i)), 'wb'))
    
    print('RMSEs:')
    for model_name in sorted(models.keys()):
        mse = ((y - predictions[model_name])**2).mean()**0.5
        print('%s: %.4f' % (model_name, mse))
        