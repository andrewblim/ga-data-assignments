from bs4 import BeautifulSoup
from porterstemmer import PorterStemmer
import datetime
import pandas as pd
import re
import simplejson
import sys
import time
import urllib2

def parse_bechdel(url, verbose=False):
    
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

def level_booleans(levels_data, colname, sep=None, zeros_ones=False):
    
    if sep is not None:
        memberships = [set(x.split(sep)) for x in levels_data]
    else:
        memberships = [set([x]) for x in levels_data]
    levels = sorted(set(reduce(lambda x,y: x | y, memberships)))
    try:
        levels.remove('')
    except:
        pass
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
                         female_words='female_words.txt',
                         female_firstnames='female_firstnames.txt',
                         verbose=False):
    
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
    
    ps = PorterStemmer()
    f = open(female_words, 'r')
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
    
    # Number of female names in the actor list: 0, 1, or 2+ (2+ will be
    # anything not flagged as 0 or 1)
    
    f = open(female_firstnames, 'r')
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

