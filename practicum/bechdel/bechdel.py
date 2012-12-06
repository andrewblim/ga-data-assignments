from bs4 import BeautifulSoup
from matplotlib.collections import RegularPolyCollection
from porterstemmer import PorterStemmer
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import re
import simplejson
import sklearn.linear_model
import sklearn.metrics
import statsmodels.api as sm
import sys
import time
import urllib2

def parse_bechdel(url, verbose=False):
    '''
    Parses a page with a list of all Bechdel films, as listed on the Bechdel
    movie list site: http://bechdeltest.com/sort/title?list=all
    Returns a dictionary mapping films' IMDB ids to a dictionary of the form
    { 'Bechdel_rating' : rating }. (More data gets added to this dictionary
    by the function attach_imdb_info().)
    '''
    
    if verbose:
        print('Processing Bechdel page...')
    
    soup = BeautifulSoup(urllib2.urlopen(url))
    film_blocks = soup.find('h2', text='Movie list').parent.find_all('div', 'movie')
    films = {}
    imdb_re = re.compile(r'http://us.imdb.com/title/tt(\d*)/')
    
    if verbose:
        print('Parsing film list...')
    
    for film_block in film_blocks:
        
        links = film_block.find_all('a')
        title = links[1].text
        imdb_url = links[0]['href']
        rating_alt = links[0].img['alt']
        if rating_alt == '[[0]]':
            rating = 'few_women'
        elif rating_alt == '[[1]]':
            rating = 'no_talk'
        elif rating_alt == '[[2]]':
            rating = 'men_talk'
        elif rating_alt == '[[3]]':
            rating = 'pass'
        else:
            raise Exception('Unrecognized rating for %s: %s' % (title, rating_alt))
        try:
            imdb_match = imdb_re.match(imdb_url)
            if imdb_match.group(1) == '':
                imdb_id = 'tt'
            else:
                imdb_id = 'tt%07d' % int(imdb_match.group(1))
        except:
            raise Exception('Unable to parse IMDB id out of url %s' % imdb_url)
        
        # manual fixes
        missing_ids = { u'Compliance': 'tt1971352',
                        u'Inside Man': 'tt0454848',
                        u'Les Bonnes Femmes': 'tt0053666',
                        u'Mama Mia!': 'tt0332938',
                        u'Primary Colors': 'tt0119942',
                        u'The Social Network': 'tt1285016',
                        u'Too Big to Fail': 'tt1742683',
                        u'What Doesn\'t Kill You': 'tt1133991',
                        }
        if title == 'Silence of the lambs':  # bad dupe
            continue
        elif imdb_id == 'tt0020642': # IMDB has this twice! using tt0020641
            imdb_id = 'tt0020641'
        elif imdb_id == 'tt':  # a handful are missing and the href just ends '/title/tt/'
            imdb_id = missing_ids[title]
        
        if imdb_id in films:
            if films[imdb_id]['Bechdel_rating'] == rating:
                print('Warning: %s (%s) appeared twice (same rating).' % \
                      (title, imdb_id))
            else:
                print('Warning: %s (%s) appeared twice with different ratings, using \'%s\' and not \'%s\'.' % \
                      (title, imdb_id, films[imdb_id]['Bechdel_rating'], rating))
            continue
        films[imdb_id] = { 'Bechdel_rating' : rating }
        
    if verbose:
        print('Films parsed, %d unique films found.' % len(films))
    
    return films

def attach_imdb_info(films, verbose=False, throttle=0):
    '''
    Given a dictionary of film data such as that returned by parse_bechdel(), 
    adds data available from IMDB using the HTTP-based OMDB API. Optional 
    throttle parameter imposes a delay between queries. 
    '''
    
    films_detailed = {}
    if verbose:
        sys.stdout.write('Adding IMDB film info via OMDB')
        sys.stdout.flush()
    
    for imdb_id in films.keys():
        
        json = urllib2.urlopen('http://www.omdbapi.com/?i=%s' % imdb_id).read()
        json_dict = simplejson.loads(json)
        if 'Error' in json_dict:
            print('ERROR on %s: %s' % (imdb_id, json_dict['Error']))
            continue
        films_detailed[imdb_id] = dict(films[imdb_id].items() + json_dict.items())
        if verbose:
            sys.stdout.write('.')
            sys.stdout.flush()
        if throttle > 0:
            time.sleep(throttle)
    
    if verbose:
        sys.stdout.write('\nAll IMDB info added.\n')
        sys.stdout.flush()
    return films_detailed

def level_booleans(levels_data, colname, sep=None, zeros_ones=False, 
                   skips=['', None]):
    '''
    Given a list/iterable of categorical data, returns a DataFrame of booleans
    indicating whether each row belongs to each category. For example if the
    input levels_data consists of ['a', 'b', 'a', 'c'], and the colname is 
    'Label', the returned DataFrame will look like:
    
    Label_a   Label_b   Label_c
    True      False     False
    False     True      False
    True      False     False
    False     False     True
    
    You can add a separator sep (can be a regexp) if each row can contain more
    than one label; for example, if levels_data was ['a,b', 'a,c'] and sep=','
    and colname is 'Label', the returned DataFrame will look like:
    
    Label_a   Label_b   Label_c
    True      True      False
    True      False     True
    
    zeros_ones will cause the matrix to return 0 and 1 instead of False and 
    True. Skips will indicate any labels to skip and not categorize. 
    '''
    
    if sep is not None:
        memberships = [set(re.split(sep, x)) for x in levels_data]
    else:
        memberships = [set([x]) for x in levels_data]
    levels = sorted(set(reduce(lambda x,y: x | y, memberships)))
    if len(skips) > 0:
        levels = filter(lambda x: x not in skips, levels)
    colnames = ['%s_%s' % (colname, x) for x in levels]
    booleans = {}
    if zeros_ones is False:
        for (level, colname) in zip(levels, colnames):
            booleans[colname] = [level in x for x in memberships]
    else:
        for (level, colname) in zip(levels, colnames):
            booleans[colname] = [1 if level in x else 0 for x in memberships]
    return pd.DataFrame(booleans)

def rating_bucket(rating):
    '''
    Given a parental guidance rating, return a string classifying that it into 
    a bucket. Combines ratings from different countries into a few buckets. 
    '''
    
    if rating in ['G', '6', '7', 'Atp', 'K-3', 'TV-G']:
        return 'general'
    elif rating in ['PG', 'M', '9', '10', '11', 'K-8', 'K-11', 'TV-PG', 'Y7']:
        return 'guidance'
    elif rating in ['PG-13', '12', '12A', '13', '13+', '14', '14A', '15', '15A', 
                    'K-12', 'K-13', 'K-15', 'M/12', 'MA15+', 'PG-12', 'R-12', 'TV-14', 'VM14']:
        return 'teen'
    elif rating in ['R', 'NC-17', '16', '18A', 'K-16', 'M/16', 'M18', 'NC-16', 'R18', 'TV-MA', 'VM18', 'X']:
        return 'adult'
    elif rating in ['Approved', 'Passed']:
        return 'pre_mpaa'
    elif rating in ['N/A', 'Not Rated', 'Unrated']:
        return 'unrated'
    else:
        return None

def generate_feature_csv(csv_out, csv_in='bechdel_full.csv', 
                         female_word_filename=None,
                         female_name_filename=None,
                         verbose=False):
    '''
    Given a csv file csv_in of features, 
    '''
    
    if verbose:
        print('Generating basic features and booleans...')
    
    raw_data = pd.read_csv(csv_in)
    data = pd.DataFrame(index=raw_data.index)
    data['Bechdel_pass'] = [1 if x == 'pass' else 0 for x in raw_data['Bechdel_rating']]
    data['Year'] = raw_data['Year']
    
    # Only 2 films have N/A votes and ratings. I think it's OK to just zero
    # their votes/ratings here
    
    data['imdbRating'] = [x if x != 'N/A' else 0 
                          for x in raw_data['imdbRating']]
    data['imdbVotes'] = [int(re.sub(',', '', x)) if x != 'N/A' else 0
                         for x in raw_data['imdbVotes']]
    
    # Adding booleans for month (not present for all releases). The thinking is
    # that movie "types" are released in seasons - blockbusters in the summer, 
    # Oscar winners near year's end - and this may impact Bechdel rating. 
    
    release_months = [datetime.datetime.strptime(x, '%d %b %Y').month \
                      if x != 'N/A' else None for x in raw_data['Released']]
    release_months = level_booleans(release_months, 'Month', zeros_ones=True)
    for col in release_months.columns:
        data[col] = release_months[col]
    
    # Booleans for parental rating. Uses the rating_bucket function to deal 
    # with the wide variety of rating types. 
    
    rating_buckets = [rating_bucket(x) for x in raw_data['Rated']]
    rating_buckets = level_booleans(rating_buckets, 'Rating', zeros_ones=True)
    for col in rating_buckets.columns:
        data[col] = rating_buckets[col]
        
    # Genre membership, this was actually easy to process because they're 
    # pretty clean
    
    genre_membership = level_booleans(raw_data['Genre'], 'Genre', sep=', ', 
                                      zeros_ones=True)
    for col in genre_membership.columns:
        data[col] = genre_membership[col]
    
    # Runtime in minutes
    
    runtime_re = re.compile('((?P<hr>\d+) h){0,1} {0,1}((?P<min>\d+) min){0,1}')
    runtime_mins = []
    runtime_na = []
    for runtime_str in raw_data['Runtime']:
        if runtime_str == 'N/A':
            runtime_mins.append(0)
            runtime_na.append(1)
        else:
            runtime_match = runtime_re.match(runtime_str)
            (runtime_hr, runtime_min) = runtime_match.group('hr'), runtime_match.group('min')
            if runtime_hr is None: runtime_hr = 0
            if runtime_min is None: runtime_min = 0
            runtime_mins.append(int(runtime_hr) * 60 + int(runtime_min))
            runtime_na.append(0)
    data['Runtime'] = runtime_mins
    data['Runtime_na'] = runtime_na
    
    if verbose:
        print('Generating word-based features (stemmed words and female names)...')
    
    # Porter-stemmed titles and plot summaries, and look for "female words" 
    # (like 'she', 'woman', etc.)
    
    if female_word_filename is not None:
        ps = PorterStemmer()
        f = open(female_word_filename, 'r')
        female_stems = set([ps.stem(x.strip().lower(), 0, len(x.strip())-1) for x in f])
        f.close()
        has_female_word = []
        for plot in raw_data['Title'] + ' ' + raw_data['Plot']:
            if plot == 'N/A':
                has_female_word.append(None)
            else:
                cur_has_female_word = 0
                plot_clean = re.sub('[^\w\s]', ' ', plot).lower().strip()
                plot_words = re.split('\s+', plot_clean)
                plot_stems = [ps.stem(x, 0, len(x)-1) for x in plot_words]
                for plot_stem in plot_stems:
                    if plot_stem in female_stems:
                        cur_has_female_word = 1
                        break
                has_female_word.append(cur_has_female_word)
        data['Female_word'] = has_female_word
    
    # Number of female names in the actor list: 0 or 1 (and anything not 
    # flagged as either should be considered 2+)
    
    if female_name_filename is not None:
        f = open(female_name_filename, 'r')
        female_nameset = set([x.strip().lower() for x in f])
        f.close()
        has_0_female_name = []
        has_1_female_name = []
        for actor_list in raw_data['Actors']:
            if actor_list == 'N/A':
                # again this issue only comes up twice
                has_0_female_name.append(0)
                has_1_female_name.append(0)
            else:
                actor_clean = re.sub('[^\w\s]', ' ', actor_list).lower().strip()
                actor_names = re.split('\s+', actor_clean)
                female_name_count = 0
                for actor_name in actor_names:
                    if actor_name in female_nameset:
                        female_name_count += 1
                if female_name_count == 0:
                    has_0_female_name.append(1)
                    has_1_female_name.append(0)
                elif female_name_count == 1:
                    has_0_female_name.append(0)
                    has_1_female_name.append(1)
                else:
                    has_0_female_name.append(0)
                    has_1_female_name.append(0)
        data['Actress_0'] = has_0_female_name
        data['Actress_1'] = has_1_female_name
    
    data.to_csv(csv_out, index=False)
    
    if verbose:
        print('Feature generation complete, output to %s.' % csv_out)

def logistic_prediction(features, response, xv_folds=10):
    '''
    Given a set of features and a response variable, runs k-fold cross-
    validated logistic regression and returns predictions and an array of 
    models (of length k, one per fold). 
    '''
    
    indices = range(len(features))
    random.shuffle(indices)
    test_indices = []
    train_indices = []
    fold_size = int(len(features)/float(xv_folds))
    for i in range(xv_folds-1):
        test_indices.append(set(indices[i*fold_size : (i+1)*fold_size]))
    test_indices.append(indices[(xv_folds-1)*fold_size : ])
    
    predictions = pd.Series([None] * len(features))
    models = []
    for test_index in test_indices:
        train_index = set(indices) - set(test_index)
        model = sklearn.linear_model.LogisticRegression(C=99999, fit_intercept=False) \
                                    .fit(features.ix[train_index],
                                         response.ix[train_index])
        predictions.ix[test_index] = model.predict_proba(features.ix[test_index])[:,1]
        # how you'd do it in statsmodels - commented out
        # model = sm.Logit(features.ix[train_index], response.ix[train_index]).fit()
        # predictions.ix[test_index] = model.predict(features.ix[test_index])
        models.append(model)
    
    return (predictions, models)

def matrix_heatmap(df, filename, labels=None):
    '''
    Generates a heatmap of the given matrix/dataframe with the provided labels.
    '''
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    img = ax.pcolor(df[::-1])
    ax.set_xticks(np.arange(len(df))+0.5)
    ax.set_yticks(np.arange(len(df))+0.5)
    if labels is None:
        try:
            labels = df.columns
        except:
            labels = range(len(df))
    ax.set_xticklabels(labels, size='xx-small', rotation='vertical')
    ax.set_yticklabels(labels[::-1], size='xx-small')
    ax.set_title('Genre correlations')
    fig.colorbar(img)
    fig.savefig(filename)
    plt.close(fig)

def graph_roc_curve(response, prediction, filename, verbose=False):
    '''
    Generates an ROC graph. 
    '''
    
    # Some code borrowed straight from the matplotlib ROC example: 
    # http://scikit-learn.org/stable/auto_examples/plot_roc.html
    
    if verbose:
        print('Generating ROC curve...')
        
    (fpr, tpr, thresholds) = sklearn.metrics.roc_curve(response, prediction)
    roc_auc = sklearn.metrics.auc(fpr, tpr)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(fpr, tpr)
    ax.plot([0,1], [0,1], 'k--')  # 45 degree line
    ax.set_xlabel('False positive rate')
    ax.set_ylabel('True positive rate')
    ax.set_title('ROC curve for Bechdel test')
    ax.legend(['AUC = %6.4f' % roc_auc], loc='lower right')
    fig.savefig(filename)
    plt.close(fig)
    
    if verbose:
        print('AUC of ROC: %6.4f' % roc_auc)
        print('ROC graph output to %s.' % filename)

def graph_precision_recall_curve(response, prediction, filename, verbose=False):
    '''
    Generates a precision-recall scatterplot. 
    '''
    
    if verbose:
        print('Generating precision-recall curve...')
    
    (precision, recall, thresholds) = sklearn.metrics.precision_recall_curve(response, prediction)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(precision, recall, marker='o', color='blue', s=4)
    ax.set_xlabel('Precision')
    ax.set_ylabel('Recall')
    ax.set_title('Precision-recall curve for Bechdel test')
    fig.savefig(filename)
    plt.close(fig)
    
    if verbose:
        print('Precision-recall graph output to %s.' % filename)

def bechdel_prediction(features_csv, genre_corr_filename, roc_filename, 
                       prec_recall_filename, bootstrap_filename, xv_folds=10, 
                       bootstrap_runs=0, verbose=False):
    '''
    The main "workhorse" function for prediction and analysis of the Bechdel
    data. Generates a correlation of genres if applicable, predicts once with
    a specified number of cross-validation folds, runs ROC and precision-
    recall analysis, then re-runs the fit many times and gives bootstrap-
    based confidence intervals for the coefficients. Uses logistic regression
    as implemented in scikit-learn. 
    '''
    
    
    if verbose:
        print('Running logistic regression on %s, %d-fold cross-validation...' % \
              (features_csv, xv_folds))
    
    features = pd.read_csv(features_csv)
    response = features.pop('Bechdel_pass')
    features.insert(0, 'const', 1)
    
    # Genre covariance
    
    if verbose:
        print('Generating genre corr heatmap to %s...' % genre_corr_filename)
    
    genre_cols = filter(lambda col: col[0:6] == 'Genre_', features.columns)
    if len(genre_cols) > 0:
        genre_cleanlabels = map(lambda col: col[6:], genre_cols)
        genre_corr = features[genre_cols].corr()
        matrix_heatmap(genre_corr, genre_corr_filename, labels=genre_cleanlabels)
    else:
        print('No genre columns found, genre corr heatmap not generated.')
    
    # Run the prediction once
    
    (prediction, models) = logistic_prediction(features, response, xv_folds=xv_folds)
    
    # ROC curve and precision-recall curve
    
    graph_roc_curve(response, prediction, roc_filename, verbose=verbose)
    graph_precision_recall_curve(response, prediction, prec_recall_filename, verbose=verbose)
    
    # Separately, run a series of logistic_prediction calls and get some 
    # bootstrapped parameters
    
    if bootstrap_runs > 0:
        
        if verbose:
            print('Running bootstrap, %d iterations (%d runs)...' % \
                  (bootstrap_runs, bootstrap_runs * xv_folds))
        bootstrap_coefs = pd.DataFrame(index=range(xv_folds * bootstrap_runs),
                                       columns=features.columns)
        aucs = []
        for i in range(bootstrap_runs):
            if verbose:
                sys.stdout.write('.')
                sys.stdout.flush()
            (cur_prediction, cur_models) = logistic_prediction(features, response, xv_folds=xv_folds)
            (fpr, tpr, thresholds) = sklearn.metrics.roc_curve(response, cur_prediction)
            aucs.append(sklearn.metrics.auc(fpr, tpr))
            for (j, cur_model) in enumerate(cur_models):
                bootstrap_coefs.ix[i*xv_folds + j] = cur_model.coef_[0]
        if verbose: 
            sys.stdout.write('\n')
            sys.stdout.flush()
        
        avg_auc = sum(aucs) / float(bootstrap_runs)
        if verbose:
            print('Average AUC: %0.6f' % avg_auc)
        
        f = open(bootstrap_filename, 'w')
        significant_coefs = []
        f.write('95% confidence levels on coefficients:\n')
        for col in bootstrap_coefs.columns:
            lower_bound = bootstrap_coefs[col].quantile(0.025)
            upper_bound = bootstrap_coefs[col].quantile(0.975)
            f.write('%20s: (%.6f, %.6f)\n' % (col, lower_bound, upper_bound))
            if (lower_bound < 0 and upper_bound < 0) or \
               (lower_bound > 0 and upper_bound > 0):
                significant_coefs.append(col)
        
        f.write('\nSignificant coefficients and their average values:\n')
        for col in significant_coefs:
            f.write('%20s: %.6f\n' % (col, bootstrap_coefs[col].mean()))
        
        f.write('\nAverage AUC: %0.6f\n' % avg_auc)
        
        f.close()
        
        if verbose:
            print('Bootstrapping complete, results written to %s.' % bootstrap_filename)

    return (prediction, response)

def reduce_features(features_csv, reduced_features_csv):
    '''
    Reduces the features of the Bechdel data to only a few important columns.
    '''
    
    features = pd.read_csv(features_csv)
    keep_cols = ['Bechdel_pass', 'Female_word', 'Actress_0', 'Actress_1']
    reduced_features = features[keep_cols]    
    reduced_features.to_csv(reduced_features_csv, index=None)