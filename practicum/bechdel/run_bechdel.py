from bechdel import *
from optparse import OptionParser
import pandas as pd
import sys

if __name__ == '__main__':
    
    bechdel_url = r'http://bechdeltest.com/sort/title?list=all'
    full_csv_filename = r'bechdel_full.csv'
    
    parser = OptionParser()
    parser.add_option('-v', '--verbose', dest='verbose',
                      action='store_true', default=True,
                      help='print verbose status to stdout')
    parser.add_option('-t', '--throttle', dest='throttle',
                      action='store', type='int', default=0,
                      help='throttle frequency of queries to OMDB')
    
    parser.add_option('--all', dest='run_all',
                      action='store_true', default=False,
                      help='run all sub-modules')
    parser.add_option('--data', dest='run_data', 
                      action='store_true', default=False,
                      help='run data scrape only')
    parser.add_option('--analysis', dest='run_analysis', 
                      action='store_true', default=False,
                      help='run analysis only')
    parser.add_option('--regression', dest='run_regression',
                      action='store_true', default=False,
                      help='run logistic regressions only')
    
    (options, args) = parser.parse_args()
    
    if not any([options.run_all, options.run_data, options.run_analysis, 
                options.run_regression]):
        print 'No options selected.'
        print 'Run with --all flag to run everything, or --help to see options.'
    
    if options.run_all or options.run_data:
        films = parse_bechdel(bechdel_url, 
                              verbose=options.verbose)
        films = attach_imdb_info(films, 
                                 verbose=options.verbose, 
                                 throttle=options.throttle)
        pd.DataFrame(films.values()).to_csv(full_csv_filename, encoding='utf-8', index=False)
    
    if options.run_all or options.run_analysis:
        data = generate_feature_csv(csv_in=full_csv_filename, 
                                    csv_out='features1.csv',
                                    verbose=options.verbose)
    
    if options.run_all or options.run_regression:
        pass