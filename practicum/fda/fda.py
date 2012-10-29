from pylab import *
import csv
import itertools
import pandas as pd
import os.path
import sys

def generate_food_detail_csv(output_filename,
                             nut_data_filename='NUT_DATA.csv',
                             fd_group_filename='FD_GROUP.csv',
                             food_des_filename='FOOD_DES.csv',
                             nutr_def_filename='NUTR_DEF.csv'):

    '''Rewrites the csv data in nut_data_filename, fd_group_filename, 
    food_des_filename, and nutr_def_filename to output_filename, one line per
    food, with a column for NDB #, food description, then one column per 
    nutrient (labeled 'nutrient_name (units)'), then columns of 0/1 for each 
    food group indicating whether the food is in that group or not. 
    
    The input csv files are assumed to be in "clean" format, i.e. you have 
    already cleaned them up from the format they're offered in by the FDA. 
    '''

    food_groups = pd.read_csv(fd_group_filename, index_col='FdGrp_Cd')
    nutrients = pd.read_csv(nutr_def_filename, index_col='Nutr_No')
    foods = pd.read_csv(food_des_filename, index_col='NDB_No')
    
    nutrient_codes = list(nutrients.index)
    food_group_codes = list(food_groups.index)
    
    with open(nut_data_filename, 'r') as f_in, \
         open(output_filename, 'w') as f_out:
        
        reader = csv.reader(f_in)
        header_in = reader.next()
        nutr_no_index = header_in.index('Nutr_No')
        nutr_val_index = header_in.index('Nutr_Val')
        
        writer = csv.writer(f_out)
        header_out = ['NDB_No', 'Long_Desc']
        header_out.extend(map(lambda x: '%s (%s)' % (nutrients.ix[x]['NutrDesc'], nutrients.ix[x]['Units']), 
                              nutrient_codes))
        header_out.extend(map(lambda x: food_groups.ix[x]['FdGrp_Desc'], 
                              food_group_codes))
        writer.writerow(header_out)
        
        sys.stdout.write('Processing foods')
        food_count = 0
    
        for k, g in itertools.groupby(reader, key=lambda x: x[0]):
            
            # Technically this and nutr_no should remain strings, but pandas 
            # insists on converting to dtype int64 (disappointingly the 
            # converters argument is no help), and it doesn't cause problems. 
            # Could cause issues in future SR releases if they start using 
            # alphanumeric NDB #s. 
            
            ndb_no = int(k)
            sys.stdout.write('.')
            sys.stdout.flush()
            
            # Each row consists of: NDB #, long description of food, a column
            # for each nutrient code, and a column for each food group code. 
            # We want None for unspecified nutrients. 
            
            row_out = [None] * (2 + len(nutrients)) + [0] * len(food_groups)
            row_out[0] = ndb_no
            row_out[1] = foods.ix[ndb_no]['Long_Desc']
            
            food_group_code = foods.ix[ndb_no]['FdGrp_Cd']
            food_group_index = 2 + len(nutrient_codes) + \
                               food_group_codes.index(food_group_code)
            row_out[food_group_index] = 1
            
            for row in g:
                nutr_no = int(row[nutr_no_index]) # same comment as ndb_no
                nutr_val = float(row[nutr_val_index])
                nutr_no_out_index = 2 + nutrient_codes.index(nutr_no)
                if row_out[nutr_no_out_index] != None:
                    raise Exception('Food %s - nutrient %s appeared twice' % (ndb_no, nutr_no))
                row_out[nutr_no_out_index] = nutr_val
            
            writer.writerow(row_out)
            
        sys.stdout.write('\nComplete.\n')
        sys.stdout.flush()

def nutrient_columns(nutr_def_filename='NUTR_DEF.csv'):
    '''Return a list of nutrient columns as produced by generate_food_detail_csv()'''
    nutrients = pd.read_csv(nutr_def_filename, index_col='Nutr_No')
    return map(lambda x: '%s (%s)' % (nutrients.ix[x]['NutrDesc'], nutrients.ix[x]['Units']), 
                                      list(nutrients.index))

def data_corrs(data, col_x, col_y, transform_x=None, transform_y=None):
    
    '''Given a pd.DataFrame populated with the output of reformat_foods (use
    read_csv()), and either a column name or a list of column names as col_x
    and col_y, returns two dataframes, one of correlations and one of the 
    number of observations used (any entries that are blank in one or the
    other are not used). 
    '''
    
    if iterable(col_x) == 0 or isinstance(col_x, str):
        col_x = [col_x]
    if iterable(col_y) == 0 or isinstance(col_y, str):
        col_y = [col_y]
    corrs = pd.DataFrame(index=col_x, columns=col_y)
    counts = pd.DataFrame(index=col_x, columns=col_y)
    
    for cx in col_x:
        for cy in col_y:
            include_rows = logical_not(logical_or(isnan(data[cx]), isnan(data[cy])))
            data_pts = data.ix[include_rows][[cx, cy]]
            if cx == cy: 
                corrs[cx][cy] = 1
            else:
                if transform_x is not None: 
                    data_pts[cx] = transform_x(data_pts[cx])
                if transform_y is not None:
                    data_pts[cy] = transform_y(data_pts[cy])
                corrs.ix[cx][cy] = corrcoef(data_pts, rowvar=0)[0][1]
            counts.ix[cx][cy] = len(data_pts)
    
    return corrs, counts

def single_nutrient_corrs(data, column, transform_x=None, transform_y=None):
    
    '''Return a data frame of all nutrient correlations versus a single
    nutrient and the number of observations for each correlation. 
    '''
    
    nutr_cols = nutrient_columns()
    (corrs, counts) = data_corrs(data, nutr_cols, column, 
                                 transform_x, transform_y)
    corrs['n'] = counts[column]
    return corrs.sort(column)

def generate_magnesium_scatterplots(data, scatter_dir, cols):
    
    '''Generates log1p scatterplots of magnesium vs. specified cols.'''
    
    mg_col = 'Magnesium, Mg (mg)'
    for col in cols:
        scatter(log1p(data[mg_col]), log1p(data[col]))
        xlabel('log1p(%s)' % mg_col)
        ylabel('log1p(%s)' % col)
        filename = '%s - %s.png' % (mg_col, col)
        savefig(os.path.join(scatter_dir, filename))
        close()
