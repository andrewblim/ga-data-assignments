from knn import *
import numpy as np
import pandas as pd
import pickle
import statsmodels.api as sm

if __name__ == '__main__':
    
    transforms = {'fixed acidity': np.log1p,
                  'volatile acidity': np.log1p,
                  'free sulfur dioxide': np.log1p,
                  'total sulfur dioxide': np.log1p,
                  'residual sugar': np.log1p,
                 }
    
    print('Reading data...')
    (y, x) = read_wine_csv('winequality-white.csv', 
                           y_col='quality',
                           transforms=transforms)
    
    print('Fitting models...')
    lr_model = linear_regression(y, x, constant=True, constant_prepend=True)
    knn1reg_model = nearest_neighbors_regressor(y, x, n_neighbors=1)
    knn1class_model = nearest_neighbors_classifier(y, x, n_neighbors=1)
    knn3reg_model = nearest_neighbors_regressor(y, x, n_neighbors=3)
    knn3class_model = nearest_neighbors_classifier(y, x, n_neighbors=3)
    knn5reg_model = nearest_neighbors_regressor(y, x, n_neighbors=5)
    knn5class_model = nearest_neighbors_classifier(y, x, n_neighbors=5)
    knn10reg_model = nearest_neighbors_regressor(y, x, n_neighbors=10)
    knn10class_model = nearest_neighbors_classifier(y, x, n_neighbors=10)
    
    print('Generating predictions...')
    predictions = pd.DataFrame({'actual': y,
                                'lr': lr_model.predict(sm.add_constant(x, prepend=True)),
                                'knn1reg': knn1reg_model.predict(x),
                                'knn1class': knn1class_model.predict(x),
                                'knn3reg': knn3reg_model.predict(x),
                                'knn3class': knn3class_model.predict(x),
                                'knn5reg': knn5reg_model.predict(x),
                                'knn5class': knn5class_model.predict(x),
                                'knn10reg': knn10reg_model.predict(x),
                                'knn10class': knn10class_model.predict(x)})
    
    print('Writing out files...')
    predictions.to_csv('predictions.csv', index=False)
    f = open('summary.txt', 'w')
    f.write(lr_model.summary().__str__() + '\n')
    f.close()
    pickle.dump(lr_model, open('lr_model.pkl', 'wb'))
    pickle.dump(knn1reg_model, open('knn1reg_model.pkl', 'wb'))
    pickle.dump(knn1class_model, open('knn1class_model.pkl', 'wb'))
    pickle.dump(knn3reg_model, open('knn3reg_model.pkl', 'wb'))
    pickle.dump(knn3class_model, open('knn3class_model.pkl', 'wb'))
    pickle.dump(knn5reg_model, open('knn5reg_model.pkl', 'wb'))
    pickle.dump(knn5class_model, open('knn5class_model.pkl', 'wb'))
    pickle.dump(knn10reg_model, open('knn10reg_model.pkl', 'wb'))
    pickle.dump(knn10class_model, open('knn10class_model.pkl', 'wb'))
    
    print('RMSEs:')
    
    lr_mse = ((y - predictions['lr'])**2).mean()**0.5
    print('Linear regression: %.4f' % lr_mse)
    
    knn1reg_mse = ((y - predictions['knn1reg'])**2).mean()**0.5
    print('1-NN regressor: %.4f' % knn1reg_mse)
    knn1class_mse = ((y - predictions['knn1class'])**2).mean()**0.5
    print('1-NN classifier: %.4f' % knn1class_mse)
    
    knn3reg_mse = ((y - predictions['knn3reg'])**2).mean()**0.5
    print('3-NN regressor: %.4f' % knn3reg_mse)
    knn3class_mse = ((y - predictions['knn3class'])**2).mean()**0.5
    print('3-NN classifier: %.4f' % knn3class_mse)
    
    knn5reg_mse = ((y - predictions['knn5reg'])**2).mean()**0.5
    print('5-NN regressor: %.4f' % knn5reg_mse)
    knn5class_mse = ((y - predictions['knn5class'])**2).mean()**0.5
    print('5-NN classifier: %.4f' % knn5class_mse)
    
    knn10reg_mse = ((y - predictions['knn10reg'])**2).mean()**0.5
    print('10-NN regressor: %.4f' % knn10reg_mse)
    knn10class_mse = ((y - predictions['knn10class'])**2).mean()**0.5
    print('10-NN classifier: %.4f' % knn10class_mse)