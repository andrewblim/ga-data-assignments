
from practicum import run_code_block
from pylab import *
import csv
import datetime
import itertools
import pandas as pd
import os
import re
import urllib2

def load_fare_data(url):
    f = csv.reader(urllib2.urlopen(url))
    f.next()
    (startdate, enddate) = f.next()[1].split('-')
    startdate = datetime.datetime.strptime(startdate, '%m/%d/%Y')
    enddate = datetime.datetime.strptime(enddate, '%m/%d/%Y')
    return (startdate, enddate, pd.read_csv(url, skiprows=2, sep=r'\s*,\s*'))

def print_fare_data_as_dict(data, filename):
    f = open(filename, 'w')
    for row in data.index:
        f.write(str(data.ix[row].to_dict()) + '\n')
    f.close()

def swipe_histogram(data, columns, filename=None, **kwargs):
    histdata = []
    for col in columns:
        histdata.extend(data[col])
    hist(histdata, **kwargs)
    if filename is None:
        show()
    else:
        savefig(filename)
    close()
    return pd.Series(histdata)

def swipe_plot(data, colx, coly, filename=None, **kwargs):
    scatter(data[colx], data[coly], **kwargs)
    if filename is None:
        show()
    else:
        savefig(filename)

def load_all_fare_data(url_file):
    all_data = {}
    f = open(url_file, 'r')
    for url in f:
        url = url.rstrip()
        print('Loading %s' % url)
        (startdate, enddate, data) = load_fare_data(url)
        all_data[(startdate, enddate)] = data
    return all_data

# Not part of the problem set. Just curious whether R170/Union Square was 
# always the most swiped 30-day unlimited remote (yep). 
def find_all_maxes(fulldata, column):
    for (startdate, enddate), data in fulldata.items():
        max_value = data[column].max()
        max_index = list(data[column]).index(max_value)
        print('%s %s %s %d' % (datetime.datetime.strftime(enddate, '%Y-%m-%d'), 
                               data.ix[max_index]['REMOTE'], 
                               data.ix[max_index]['STATION'], 
                               max_value))

def transform_all_fare_data(fulldata, filename):
    f = csv.writer(open(filename, 'w'))
    f.writerow(['station_name','date','count'])
    for (startdate, enddate), data in sorted(fulldata.items()):
        enddate_str = datetime.datetime.strftime(enddate, '%Y-%m-%d')
        for i in data.index:
            f.writerow([data.ix[i]['STATION'],
                        enddate_str,
                        sum(data.ix[i][2:])])

def reduce_by_station(input_filename, output_filename, dates):
    
    f_in = csv.reader(open(input_filename, 'r'))
    f_in.next()
    f_out = csv.writer(open(output_filename, 'w'))
    
    date_strs = [datetime.datetime.strftime(d, '%Y-%m-%d') for d in dates]
    header = ['station_name', 'count_average']
    header.extend(map(lambda x: 'count_week_' + x, date_strs))
    f_out.writerow(header)
    
    for key, group in itertools.groupby(f_in, lambda x: x[0]):
        
        counts = [None] * len(date_strs)
        for row in group:
            (station, date_str, count) = row
            i = date_strs.index(date_str)
            if counts[i] == None:
                counts[i] = 0
            counts[i] += int(count)
        
        row = [key]
        counts_clean = filter(lambda x: x is not None, counts)
        row.append(sum(counts_clean)/float(len(counts_clean)))
        row.extend(counts)
        f_out.writerow(row)

def cross_tabulate(data, col1, col2):
    
    median1 = data[col1].median()
    median2 = data[col2].median()
    lolo = 0
    lohi = 0
    hilo = 0
    hihi = 0
    for i in data.index:
        val1 = data.ix[i][col1]
        val2 = data.ix[i][col2]
        if val1 <= median1:
            if val2 <= median2: 
                lolo += 1
            else:
                lohi += 1
        else:
            if val2 <= median2:
                hilo += 1
            else:
                hihi += 1
    print('%s below, %s below: %d' % (col1, col2, lolo))
    print('%s below, %s above: %d' % (col1, col2, lohi))
    print('%s above, %s below: %d' % (col1, col2, hilo))
    print('%s above, %s above: %d' % (col1, col2, hihi))


if __name__ == '__main__':
    
    # dependencies for problems 2-5, 9
    if any(map(run_code_block, [2,3,4,5,9])):
        (startdate, enddate, data) = load_fare_data('http://mta.info/developers/data/nyct/fares/fares_121006.csv')
    
    # dependencies for problems 7-8
    if any(map(run_code_block, [7,8])):
        fulldata = load_all_fare_data('fareurls.txt')
        print
    
    # problem 2
    if run_code_block(2):
        print_fare_data_as_dict(data, 'dictionary_dump.txt')
        print('Problem 2: Dictionaries printed to dictionary_dump.txt.')
        print
    
    # problem 3
    if run_code_block(3):
        columns = ['30-D AFAS/RMF UNL', '30-D UNL', 'AIRTRAIN 30-D']
        histdata = swipe_histogram(data, columns, filename='problem3.png', bins=100)
        print('Problem 3:')
        print('Max (outlier): %d' % histdata.max())
        print('Mean: %0.4f' % histdata.mean())
        print('Median: %d' % histdata.median())
        outlier_index = list(data['30-D UNL']).index(histdata.max())  # it's in 30-D UNL, I checked
        print('Outlier info:')
        print data.ix[outlier_index]
        print('Graph saved to problem3.png')
        print
    
    # problem 4
    if run_code_block(4):
        columns = ['PATH 2-T']
        swipe_histogram(data, columns, filename='problem4_path.png', bins=100)
        columns = ['STUDENTS']
        swipe_histogram(data, columns, filename='problem4_student.png', bins=100)
        print('Problem 4: graphs saved to problem4_path.png and problem4_student.png')
        print
    
    # problem 5
    if run_code_block(5):
        swipe_plot(data, '30-D UNL', 'FF', filename='problem5.png')
        print('Problem 5: graph saved to problem5.png')
        print
    
    # problem 7, also prerequisite for problem 8
    if run_code_block(7):
        transform_all_fare_data(fulldata, 'transformed_data.csv')
        print('Problem 7: transformed data saved to transformed_data.csv')
        print
    
    # problem 8
    if run_code_block(8):
        os.system('awk \'NR == 1 { print } NR > 1 { print | "sort" }\' transformed_data.csv > sorted_data.csv')
        enddates = sorted([x[1] for x in fulldata.keys()])
        print('Problem 8: sorted data saved to sorted_data.csv')
        reduce_by_station('sorted_data.csv', 'grouped_data.csv', enddates)
        print('Problem 8: grouped data saved to grouped_data.csv')
        print
    
    # problem 9
    if run_code_block(9):
        print('Problem 9:')
        cross_tabulate(data, '30-D UNL', 'FF')
        print
        