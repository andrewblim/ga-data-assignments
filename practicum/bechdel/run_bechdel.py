from bechdel import *
from optparse import OptionParser
import pandas as pd
import sys

if __name__ == '__main__':
    
    # input files
    
    bechdel_url = r'http://bechdeltest.com/sort/title?list=all'
    female_name_filename = r'female_firstnames.txt'
    female_word_filename = r'female_words.txt'
    
    # intermediate files
    
    full_csv_filename = r'bechdel_full.csv'
    features_csv_filename = r'features.csv'
    features2_csv_filename = r'features_reduced.csv'
    
    # output files
    
    genre_corr_filename = r'genre_corr.png'
    roc_filename = r'roc.png'
    prec_recall_filename = r'precision_recall.png'
    bootstrap_filename = r'bootstrap.txt'
    
    genre_corr2_filename = r'genre_corr_reduced.png'
    roc2_filename = r'roc_reduced.png'
    prec_recall2_filename = r'precision_recall_reduced.png'
    bootstrap2_filename = r'bootstrap_reduced.txt'
    
    parser = OptionParser()
    parser.add_option('-q', '--quiet', dest='verbose',
                      action='store_false', default=True,
                      help='run quietly (less verbose statuses)')
    parser.add_option('-t', '--throttle', dest='throttle',
                      action='store', type='int', default=0,
                      help='throttle frequency of queries to OMDB')
    
    parser.add_option('--all', dest='run_all',
                      action='store_true', default=False,
                      help='run all sub-modules')
    parser.add_option('--all-but-data', dest='run_all_but_data',
                      action='store_true', default=False,
                      help='run all sub-modules except data scrape')
    parser.add_option('--data', dest='run_data', 
                      action='store_true', default=False,
                      help='run data scrape only')
    parser.add_option('--features', dest='run_features', 
                      action='store_true', default=False,
                      help='run feature generation only')
    parser.add_option('--prediction', dest='run_prediction',
                      action='store_true', default=False,
                      help='run logistic regression-based prediction only')
    parser.add_option('--reduced-prediction', dest='run_reduced_prediction',
                      action='store_true', default=False,
                      help='run logistic regression-based prediction on reduced features only')
    
    (options, args) = parser.parse_args()
    
    if not any([options.run_all, options.run_all_but_data, options.run_data, 
                options.run_features, options.run_prediction,
                options.run_reduced_prediction]):
        print 'No options selected.'
        print 'Run with --all flag to run everything, or --help to see options.'
    
    if options.run_all or options.run_data:
        films = parse_bechdel(bechdel_url, 
                              verbose=options.verbose)
        films = attach_imdb_info(films, 
                                 verbose=options.verbose, 
                                 throttle=options.throttle)
        pd.DataFrame(films.values()).to_csv(full_csv_filename, encoding='utf-8', index=False)
    
    if any([options.run_all, options.run_all_but_data, options.run_features]):
        data = generate_feature_csv(csv_in=full_csv_filename, 
                                    csv_out=features_csv_filename,
                                    female_name_filename=female_name_filename,
                                    female_word_filename=female_word_filename,
                                    verbose=options.verbose)
    
    if any([options.run_all, options.run_all_but_data, options.run_prediction]):
        bechdel_prediction(features_csv=features_csv_filename,
                           genre_corr_filename=genre_corr_filename,
                           roc_filename=roc_filename,
                           prec_recall_filename=prec_recall_filename,
                           bootstrap_filename=bootstrap_filename,
                           bootstrap_runs=100,
                           verbose=options.verbose)
    
    if any([options.run_all, options.run_all_but_data, 
            options.run_reduced_prediction]):
        reduce_features(features_csv_filename, 
                        features2_csv_filename)
        bechdel_prediction(features_csv=features2_csv_filename,
                           genre_corr_filename=genre_corr2_filename,
                           roc_filename=roc2_filename,
                           prec_recall_filename=prec_recall2_filename,
                           bootstrap_filename=bootstrap2_filename,
                           bootstrap_runs=100,
                           verbose=options.verbose)
        