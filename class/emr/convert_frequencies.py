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
    print_frequencies(old_freq, new_freq)
    print_frequencies(old_freq, new_freq, omit_s=True)