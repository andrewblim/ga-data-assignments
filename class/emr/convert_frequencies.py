import re
import sys
import os
import os.path

def convert_frequencies(directory='emr_output'):
    
    old_freq = [0] * 26
    new_freq = [0] * 26
    for filename in os.listdir(directory):
        if re.match('^part', filename):
            with open(os.path.join(directory, filename), 'r') as f:
                for line in f:
                    (year, count_array_str) = line.split('\t')
                    year = int(year)
                    count_array_str = re.sub('[\[\]]', '', count_array_str)
                    count_array = map(int, count_array_str.split(','))
                    if year >= 1938 and year <= 1948:
                        for c in range(26):
                            old_freq[c] += count_array[c]
                    else:
                        for c in range(26):
                            new_freq[c] += count_array[c]
    
    old_total = float(sum(old_freq))
    new_total = float(sum(new_freq))
    for c in range(26):
        old_freq[c] /= old_total
        new_freq[c] /= new_total
    return old_freq, new_freq

def mean_squared_error(x, y):
    if len(x) != len(y):
        raise Exception('mean_squared_error given two iterables of different lengths')
    mse = 0
    for i in range(len(x)):
        mse += (x[i] - y[i]) ** 2
    return mse / float(len(x))

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        old_freq, new_freq = convert_frequencies()
    else:
        old_freq, new_freq = convert_frequencies(sys.argv[1])
    
    # remove S and readjust frequencies
    old_s = old_freq.pop(18)
    old_freq = [x/(1.0 - old_s) for x in old_freq]
    new_s = new_freq.pop(18)
    new_freq = [x/(1.0 - new_s) for x in new_freq]
    
    scrabble_freq_count = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,6,4,2,2,1,2,1]
    scrabble_freq = [x/float(sum(scrabble_freq_count)) for x in scrabble_freq_count]
    wwf_freq_count = [9,2,2,5,13,2,3,4,8,1,1,4,2,5,8,2,1,6,7,4,2,2,1,2,1]
    wwf_freq = [x/float(sum(wwf_freq_count)) for x in wwf_freq_count]
    
    letters = 'abcdefghijklmnopqrtuvwxyz'
    print('    %9s %9s %9s %9s' % ('Scrabble', 'WWF', '1938-1948', '2005-'))
    for i in range(len(letters)):
        c = letters[i]
        print('%s : %8.2f%% %8.2f%% %8.2f%% %8.2f%%' % 
              (c, scrabble_freq[i] * 100, wwf_freq[i] * 100, old_freq[i] * 100, new_freq[i] * 100))
    
    era_mse = mean_squared_error(old_freq, new_freq)
    scrabble_old_mse = mean_squared_error(scrabble_freq, old_freq)
    scrabble_new_mse = mean_squared_error(scrabble_freq, new_freq)
    wwf_old_mse = mean_squared_error(wwf_freq, old_freq)
    wwf_new_mse = mean_squared_error(wwf_freq, new_freq)
    
    print('MSE between eras: %f' % (era_mse * 10000))
    print('Scrabble MSE vs. old data: %f' % (scrabble_old_mse * 10000))
    print('Scrabble MSE vs. new data: %f' % (scrabble_new_mse * 10000))
    print('WWF MSE vs. old data: %f' % (wwf_old_mse * 10000))
    print('WWF MSE vs. new data: %f' % (wwf_new_mse * 10000))
    