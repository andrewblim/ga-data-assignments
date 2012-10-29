from fda import *
from optparse import OptionParser

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
    
    (options, args) = parser.parse_args()
    
    filename = 'nutr_by_food.csv'
    scatter_dir = 'scatter'
    
    if options.food_detail is True or options.run_all is True:
        generate_food_detail_csv(filename)
        print('%s generated.' % filename)
        
    if any([options.run_all, options.magnesium_corrs, options.magnesium_scatter]):
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
        print('Magnesium scatterplots generated to %s.' % scatter_dir)