from knn import *
import numpy as np
import statsmodels.api as sm
import sys

if __name__ == '__main__':
    
    if len(sys.argv) == 2 and sys.argv[1] == 'histograms':
        generate_histograms('winequality-white.csv', 'histograms', bins=20)
    
    else:
        
        transforms = {'fixed acidity': np.log1p,
                      'volatile acidity': np.log1p,
                      'free sulfur dioxide': np.log1p,
                      'total sulfur dioxide': np.log1p,
                      'residual sugar': np.log1p}
        
        models = {'lr': lambda y, x: linear_regression(y, x, constant=True, constant_prepend=True),
                  'knn3reg': lambda y, x: nearest_neighbors_regressor(y, x, n_neighbors=3),
                  'knn3class': lambda y, x: nearest_neighbors_classifier(y, x, n_neighbors=3),
                  'knn10reg': lambda y, x: nearest_neighbors_regressor(y, x, n_neighbors=10),
                  'knn10class': lambda y, x: nearest_neighbors_classifier(y, x, n_neighbors=10)}
        
        predict_override = {'lr': lambda predictor, x: getattr(predictor, 'predict')(sm.add_constant(x, prepend=True))}
                      
        run_all_predictors(input_filename='winequality-white.csv',
                           output_dir='quality',
                           response='quality',
                           transforms=transforms,
                           models=models,
                           predict_override=predict_override)
        
        # classifiers aren't reasonable for continuous pH prediction
        del models['knn3class']
        del models['knn10class']
        
        run_all_predictors(input_filename='winequality-white.csv',
                          output_dir='pH',
                          response='pH',
                          predictors=['citric acid',
                                      'free sulfur dioxide',
                                      'total sulfur dioxide',
                                      'alcohol'],
                          transforms=transforms,
                          models=models,
                          predict_override=predict_override)