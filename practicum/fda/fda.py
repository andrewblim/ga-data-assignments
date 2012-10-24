from pylab import *
import csv
import itertools
import pandas as pd
import sys

def reformat_foods(output_filename,
                   nut_data_filename='NUT_DATA.csv',
                   fd_group_filename='FD_GROUP.csv',
                   food_des_filename='FOOD_DES.csv',
                   nutr_def_filename='NUTR_DEF.csv'):

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


def get_correlations(data, col_x, col_y, transform_x=None, transform_y=None):
    
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