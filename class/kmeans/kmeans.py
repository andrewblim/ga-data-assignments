from mpl_toolkits.basemap import Basemap
from sklearn.cluster import KMeans
import csv
import matplotlib.cm
import matplotlib.pyplot as plt
import os
import pandas as pd
import pickle

def read_plant_data(plants_csv, state_abbr_csv, verbose=True):
    
    if verbose: print('Reading data...')
    state_abbr_reader = csv.reader(open(state_abbr_csv, 'r'))
    state_dict = {}
    for row in state_abbr_reader:
        state_dict[row[0]] = row[1]
    
    habitats = { abbr: [] for abbr in state_dict.keys() }
    habitats['species'] = []
    plants_reader = csv.reader(open(plants_csv, 'r'))
    for row in plants_reader:
        habitats['species'].append(row[0])
        states = set(row[1:])
        for abbr in state_dict.keys():
            if abbr in states: habitats[abbr].append(1)
            else: habitats[abbr].append(0)
    
    return (pd.DataFrame(habitats), state_dict)

def plant_cluster(habitat_data, state_dict, output_dir=None, n_clusters=8, 
                  maps=False, name=None, verbose=True, **kwargs):
    
    model = KMeans(n_clusters, **kwargs).fit(habitat_data[sorted(state_dict.keys())])
    pred = model.labels_
    probs = []
    if verbose: 
        if name is None: print('Fitting model %s...' % output_dir)
        else: print('Fitting model %s (output to dir %s)...' % (name, output_dir))
    for i in range(n_clusters):
        n_preds = len(habitat_data[pred == i])
        probs.append(sorted([(state, sum(habitat_data[state][pred == i]), n_preds)
                             for state in state_dict.keys()], 
                            key=lambda x: x[1],
                            reverse=True))
    if output_dir is not None:
        try: os.mkdir(output_dir)
        except OSError: pass
        pickle.dump(model, open(os.path.join(output_dir, 'model.pkl'), 'wb'))
        pickle.dump(probs, open(os.path.join(output_dir, 'probs.pkl'), 'wb'))
        if maps:
            probs_heatmap(probs, state_dict, output_dir=output_dir, verbose=verbose)
    return (model, probs)

def cluster_variance_explained(habitat_data, state_dict, models, names=None, verbose=True):
    
    data = habitat_data[sorted(state_dict.keys())]
    variance = ((data.mean() - data)**2).sum().sum()
    explained_variance = []
    j = 0
    for model in models:
        if verbose:
            if names is not None:
                print('Calculating explained variance of %s...' % names[j])
            else:
                print('Calculating explained variance of model %d...' % j)
        model_variance = 0
        for i in range(len(model.labels_)):
            center = model.cluster_centers_[model.labels_[i]]
            model_variance += ((data.ix[i] - center)**2).sum()
        explained_variance.append((variance - model_variance) / float(variance))
        j += 1
    if names == None:
        return explained_variance
    else:
        return dict(zip(names, explained_variance))

def probs_heatmap(probs, state_dict, output_dir='.', verbose=True):
    
    try: os.mkdir(output_dir)
    except OSError: pass
    
    for (cluster_i, cluster) in enumerate(probs):
        
        if verbose: print('Initializing map for cluster %d/%d...' % (cluster_i+1, len(probs)))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        m = Basemap(width=12000000,
                    height=9000000,
                    projection='lcc',
                    resolution='l',
                    lat_1=45.,
                    lat_2=55,
                    lat_0=50,
                    lon_0=-115.,
                    ax=ax)
        m.drawcoastlines()
        
        if verbose: print('Reading shapefiles...')
        m.readshapefile('shapefiles/us', 'us', drawbounds=False)
        m.readshapefile('shapefiles/canada', 'canada', drawbounds=False)
        
        for (abbr, count, n_preds) in cluster:
            
            region = state_dict[abbr]
            # a few hacky fixes for regions
            if region == 'Newfoundland' or region == 'Labrador':
                # ignore, no way to do this without regrouping the raw data as
                # you'll have some in one but not the other and some in both
                continue
            elif region == 'Qu\xe9bec':
                region = 'Quebec'
            elif region == 'Yukon':
                region = 'Yukon Territory'
            prob = count / float(n_preds)
            
            for i in range(len(m.canada)):
                if m.canada_info[i]['NAME'] == region:
                    (x, y) = zip(*m.canada[i])
                    plt.fill(x, y, color=(1-prob, 1-prob, 1))
            for i in range(len(m.us)):
                if m.us_info[i]['NAME'] == region:
                    (x, y) = zip(*m.us[i])
                    plt.fill(x, y, color=(1-prob, 1-prob, 1))
        
        ax.set_title('Cluster %d (n = %d)' % (cluster_i, cluster[0][2]))
        filename = os.path.join(output_dir, 'cluster%d.png' % cluster_i)
        plt.savefig(filename)
        if verbose: print('Written to %s.' % filename)
        plt.close(fig)