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
    
    old_freq = dict(zip('abcdefghijklmnopqrstuvwxyz', old_freq))
    new_freq = dict(zip('abcdefghijklmnopqrstuvwxyz', new_freq))
    return old_freq, new_freq

def print_frequencies(old_freq, new_freq, omit_s=False):
    if not omit_s:
        print 'old'
        for k in sorted(old_freq.keys()):
            print '%s : %2.2f' % (k, old_freq[k] * 100)
        print 'new'
        for k in sorted(new_freq.keys()):
            print '%s : %2.2f' % (k, new_freq[k] * 100)
    else:
        print 'old, omitting s'
        for k in sorted(old_freq.keys()):
            if k != 's':
                print '%s : %2.2f' % (k, (old_freq[k] / (1.0 - old_freq['s'])) * 100)
        print 'new, omitting s'
        for k in sorted(new_freq.keys()):
            if k != 's':
                print '%s : %2.2f' % (k, (new_freq[k] / (1.0 - new_freq['s'])) * 100)

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        old_freq, new_freq = convert_frequencies()
    else:
        old_freq, new_freq = convert_frequencies(sys.argv[1])
    
    scrabble_freq = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,6,4,2,2,1,2,1]
    scrabble_freq_p = [x/float(sum(scrabble_freq)) for x in scrabble_freq]
    scrabble_old_mse = 0
    for c in range(25):
        scrabble_old_mse += (scrabble_freq_p[c] - old_freq.values()[c])**2
    scrabble_old_mse /= float(sum(scrabble_freq))
    scrabble_new_mse = 0
    for c in range(25):
        scrabble_new_mse += (scrabble_freq_p[c] - new_freq.values()[c])**2
    scrabble_new_mse /= float(sum(scrabble_freq))
    
    wwf_freq = [9,2,2,5,13,2,3,4,8,1,1,4,2,5,8,2,1,6,7,4,2,2,1,2,1]
    wwf_freq_p = [x/float(sum(wwf_freq)) for x in wwf_freq]
    wwf_old_mse = 0
    for c in range(25):
        wwf_old_mse += (wwf_freq_p[c] - old_freq.values()[c])**2
    wwf_old_mse /= float(sum(wwf_freq))
    wwf_new_mse = 0
    for c in range(25):
        wwf_new_mse += (wwf_freq_p[c] - new_freq.values()[c])**2
    wwf_new_mse /= float(sum(wwf_freq))
    
    print_frequencies(old_freq, new_freq, omit_s=True)
    print 'Scrabble MSE vs. old data: %f' % (scrabble_old_mse * 10000)
    print 'Scrabble MSE vs. new data: %f' % (scrabble_new_mse * 10000)
    print 'WWF MSE vs. old data: %f' % (wwf_old_mse * 10000)
    print 'WWF MSE vs. new data: %f' % (wwf_new_mse * 10000)
    