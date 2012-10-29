from fda import *
from optparse import OptionParser
import os.path
import pickle

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('--all-problems', action='store_true', 
                      dest='run_all',
                      help='run all exercises')
    parser.add_option('--food-detail', action='store_true',
                      dest='food_detail',
                      help='generate food detail file to nutr_by_food.csv')
    parser.add_option('--magnesium-corrs', action='store_true',
                      dest='magnesium_corrs',
                      help='generate log-transformed magnesium correlations')
    parser.add_option('--magnesium-scatter', action='store_true',
                      dest='magnesium_scatter',
                      help='generate log-transformed magnesium scatterplots')
    parser.add_option('--full-reg', action='store_true', 
                      dest='full_reg',
                      help='generate log-transformed nutrient regression')
    parser.add_option('--full-reg-variation', action='store_true', 
                      dest='full_reg_variation',
                      help='see which features in the full regression generate variation')
    parser.add_option('--bootstrap', action='store_true', 
                      dest='bootstrap',
                      help='generate coefficients from bootstrap')
    parser.add_option('--reduced-reg', action='store_true', 
                      dest='reduced_reg',
                      help='generate log-transformed nutrient regression on fewer features')
    
    (options, args) = parser.parse_args()
    
    nutr_filename = 'nutr_by_food.csv'
    mg_label = 'Magnesium, Mg (mg)'
    scatter_dir = 'scatter'
    reg_dir = 'regressions'
    
    # Problem 1
    
    if any([options.food_detail, options.run_all]):
        generate_food_detail_csv(nutr_filename)
        print('Food detail generated to %s.' % nutr_filename)
    
    # read in data from problem 1 - prerequisite for remaining problems
    
    if any([options.run_all, options.magnesium_corrs, 
            options.magnesium_scatter, options.full_reg,
            options.bootstrap, options.reduced_reg]):
        data = pd.read_csv(nutr_filename)
    
    # Correlation diagnostic - see what is correlated to magnesium content. 
    # Used to figure out what to plot in problem 2. 
    
    if options.magnesium_corrs is True:
        corrs = single_nutrient_corrs(data, 
                                      mg_label, 
                                      transform_x=log1p, 
                                      transform_y=log1p)
        print(corrs)
    
    # Problem 2
    
    if options.magnesium_scatter is True or options.run_all is True: 
        scatter_cols = ['Potassium, K (mg)', 
                        'Phosphorus, P (mg)', 
                        'Manganese, Mn (mg)', 
                        'Fatty acids, total trans (g)']
        generate_magnesium_scatterplots(data, scatter_dir, scatter_cols)
        print('Magnesium scatterplots generated to directory %s.' % scatter_dir)
    
    # label_cols are the nutrients found on a standard food label
    
    if any([options.full_reg, options.bootstrap, 
            options.reduced_reg, options.run_all]):
        label_cols = ['Fatty acids, total monounsaturated (g)',
                      'Fatty acids, total polyunsaturated (g)',
                      'Fatty acids, total saturated (g)',
                      'Fatty acids, total trans (g)',
                      'Cholesterol (mg)',
                      'Sodium, Na (mg)',
                      'Potassium, K (mg)',
                      'Fiber, total dietary (g)',
                      'Sugars, total (g)',
                      'Protein (g)']
    
    # Problem 3
    
    if options.full_reg is True or options.run_all is True:
        
        results = regress_log1p_dataframe(data, mg_label, label_cols)
        
        full_reg_path = os.path.join(reg_dir, 'full_reg.txt')
        full_reg_pickle_path = os.path.join(reg_dir, 'full_reg.pkl')
        f = open(full_reg_path, 'w')
        f.write(results.summary().__str__() + '\n')
        f.close()
        print('Regression summary output to %s.' % full_reg_path)
        f = open(full_reg_pickle_path, 'wb')
        pickle.dump(results, f)
        f.close()
        print('Regression results pickled to %s.' % full_reg_pickle_path)
        
        mean_error = abs(results.resid).mean()
        mean_expm1_error = abs(expm1(results.model.endog) - expm1(results.predict())).mean()
        print('Average absolute error of log1p(magnesium): %f' % mean_error)
        print('Average absolute error of magnesium: %f' % mean_expm1_error)
    
    # Check which coefficients in the full regression generate variation in
    # predicted magnesium. 
    
    if options.full_reg_variation is True:
        
        full_reg_pickle_path = os.path.join(reg_dir, 'full_reg.pkl')
        results = pickle.load(open(full_reg_pickle_path, 'rb'))
        print('%40s %12s %12s' % ('Feature', 'Mean * coef', 'SD * coef'))
        for i in range(len(results.model.exog_names)):
            print('%40s %12.4f %12.4f' % (results.model.exog_names[i],
                                          results.model.exog[i].mean() * results.params[i],
                                          results.model.exog[i].std() * results.params[i]))
    
    # Problems 4 and 5
    
    if options.bootstrap is True or options.run_all is True:
        
        coefs = bootstrap_log1p_dataframe(data,
                                          mg_label, 
                                          label_cols, 
                                          sample_frac=0.1, 
                                          n=1000)
        coefs.to_csv('bootstrap_data/coefs.csv', index=False)
        print('Bootstrap coefs generated to bootstrap_data/coefs.csv.')
        print('95% confidence interval based on bootstrapping (sample 10% of population):')
        for col in coefs.columns:
            print('%40s : [%8.4f, %8.4f]' % (col, 
                                             coefs[col].quantile(0.025), 
                                             coefs[col].quantile(0.975)))
    
    if options.reduced_reg is True or options.run_all is True:
        sig_cols = ['Sodium, Na (mg)',
                    'Potassium, K (mg)',
                    'Fiber, total dietary (g)',
                    'Phosphorus, P (mg)',
                    'Manganese, Mn (mg)',
                    'Vitamin B-12 (mcg)']
        reduced_results = regress_log1p_dataframe(data, 'Magnesium, Mg (mg)', sig_cols)
        f = open(os.path.join(reg_dir, 'reduced_reg.txt'), 'w')
        f.write(reduced_results.summary().__str__() + '\n')
        f.close()
        reduced_results.save
        f = open(os.path.join(reg_dir, 'reduced_reg.pkl'), 'wb')
        pickle.dump(reduced_results, f)
        f.close()
        
        mean_error = abs(reduced_results.resid).mean()
        mean_expm1_error = abs(expm1(reduced_results.model.endog) - \
                               expm1(reduced_results.predict())).mean()
        print('Average absolute error log1p(magnesium): %f' % mean_error)
        print('Average absolute error magnesium: %f' % mean_expm1_error)
        print('Full regression files generated to dir %s.' % reg_dir)
        
        rdata = reduce_data(data, label_cols + ['Magnesium, Mg (mg)'])
        X = sm.add_constant(log1p(rdata[sig_cols]), prepend=False)
        mean_error = abs(reduced_results.predict(X) - log1p(rdata['Magnesium, Mg (mg)'])).mean()
        mean_expm1_error = abs(rdata['Magnesium, Mg (mg)'] - \
                               expm1(reduced_results.predict(X))).mean()
        print('Average absolute error log1p(magnesium): %f' % mean_error)
        print('Average absolute error magnesium: %f' % mean_expm1_error)