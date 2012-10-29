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
    parser.add_option('--bootstrap', action='store_true', 
                      dest='bootstrap',
                      help='generate coefficients from bootstrap')
    parser.add_option('--reduced-reg', action='store_true', 
                      dest='reduced_reg',
                      help='generate log-transformed nutrient regression on fewer features')
    
    (options, args) = parser.parse_args()
    
    filename = 'nutr_by_food.csv'
    scatter_dir = 'scatter'
    reg_dir = 'regressions'
    
    if options.food_detail is True or options.run_all is True:
        generate_food_detail_csv(filename)
        print('%s generated.' % filename)
        
    if any([options.run_all, options.magnesium_corrs, 
            options.magnesium_scatter, options.full_reg,
            options.bootstrap, options.reduced_reg]):
        data = pd.read_csv(filename)
        
    if options.magnesium_corrs is True:
        corrs = single_nutrient_corrs(data, 'Magnesium, Mg (mg)', 
                                      transform_x=log1p, transform_y=log1p)
        print(corrs)
        
    if options.magnesium_scatter is True or options.run_all is True: 
        cols = ['Potassium, K (mg)', 
                'Phosphorus, P (mg)', 
                'Manganese, Mn (mg)', 
                'Fatty acids, total trans (g)']
        generate_magnesium_scatterplots(data, scatter_dir, cols)
        print('Magnesium scatterplots generated to dir %s.' % scatter_dir)
    
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
                      'Calcium, Ca (mg)',
                      'Iron, Fe (mg)',
                      'Zinc, Zn (mg)',
                      'Phosphorus, P (mg)',
                      'Copper, Cu (mg)',
                      'Manganese, Mn (mg)',
                      'Thiamin (mg)',
                      'Riboflavin (mg)',
                      'Niacin (mg)',
                      'Vitamin A, RAE (mcg_RAE)',
                      'Vitamin B-6 (mg)',
                      'Vitamin B-12 (mcg)',
                      'Vitamin C, total ascorbic acid (mg)']
    
    if options.full_reg is True or options.run_all is True:
        results = regress_log1p_dataframe(data, 'Magnesium, Mg (mg)', label_cols)
        f = open(os.path.join(reg_dir, 'full_reg.txt'), 'w')
        f.write(results.summary().__str__() + '\n')
        f.close()
        results.save
        f = open(os.path.join(reg_dir, 'full_reg.pkl'), 'wb')
        pickle.dump(results, f)
        f.close()
        mean_error = abs(results.resid).mean()
        mean_expm1_error = abs(expm1(results.model.endog) - expm1(results.predict())).mean()
        print('Average absolute error log1p(magnesium): %f' % mean_error)
        print('Average absolute error magnesium: %f' % mean_expm1_error)
        print('Full regression files generated to dir %s.' % reg_dir)
    
    if options.bootstrap is True or options.run_all is True:
        coefs = bootstrap_log1p_dataframe(data, 'Magnesium, Mg (mg)', 
                                          label_cols, 
                                          sample_frac=0.25, n=1000)
        coefs.to_csv('bootstrap_data/coefs.csv', index=False)
        for col in coefs.columns:
            print('%40s : [%8.4f, %8.4f]' % (col, 
                                             coefs[col].quantile(0.025), 
                                             coefs[col].quantile(0.975)))
        print('Bootstrap coefs generated to bootstrap_data/coefs.csv.')
    
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