from kmeans import *
from optparse import OptionParser
import sys

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('-q', '--quiet', 
                      action='store_false', dest='verbose', default=True,
                      help='don\'t print status messages to stdout')
    parser.add_option('--maps',
                      action='store_true', dest='maps', default=False,
                      help='generate heatmaps into k-means directories (can be slow)')
    
    (options, args) = parser.parse_args()
    
    if len(args) == 2:
        (k_lower, k_upper) = (int(args[0]), int(args[1]))
    elif len(args) == 1: 
        k_lower = k_upper = int(args[0])
    else:
        (k_lower, k_upper) = (1, 5)
    
    (habitat_data, state_dict) = read_plant_data('plants/plants.csv', 
                                                 'plants/stateabbr.csv',
                                                 verbose=options.verbose)
                                                 
    models = []
    probs = []
    model_names=[]
    for i in range(k_lower, k_upper+1):
        model_name = '%02d-means' % i
        (model, prob) = plant_cluster(habitat_data, state_dict, 
                                      output_dir=model_name,
                                      n_clusters=i,
                                      name=model_name,
                                      verbose=options.verbose,
                                      maps=options.maps)
        models.append(model)
        probs.append(prob)
        model_names.append(model_name)
    
    explained_variance = cluster_variance_explained(habitat_data, state_dict, models,
                                                    names=model_names,
                                                    verbose=options.verbose)
    if isinstance(explained_variance, dict):
        for model_name in sorted(explained_variance.keys()):
            print('Variance explained by %s: %0.4f' % (model_name, explained_variance[model_name]))
    else:
        for i in range(len(explained_variance)):
            print('Variance explained by model %d: %0.4f' % (model_name, explained_variance[i]))