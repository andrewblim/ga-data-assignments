from mrjob.job import MRJob
import re
import urllib2

def read_dictionary(dict_handle):
    word_dict = {}
    for word in dict_handle:
        word_dict[word.strip().lower()] = True
    return word_dict

word_dict = read_dictionary(urllib2.urlopen('https://s3.amazonaws.com/andrewblim-ngrams/twl06-analysis/TWL06.txt'))

class ScrabbleLetterCounter(MRJob):

    def letter_frequencies(self, key, line):
        try:
            (word, year, word_count, corpus_count) = line.split()
            letter_count = [0] * 26
            word = re.sub('_(NOUN|VERB|ADJ|ADV|PRON|DET|ADP|NUM|CONJ|PRT|ROOT|START|END)_{0,1}', '', word)
            word = word.lower()
            if word_dict.has_key(word):
                for c in word:
                    letter_count[ord(c) - 97] += int(word_count)
                yield int(year), letter_count
        except:
            pass
    
    def sum_frequencies(self, year, letter_counts):
        total_letter_count = [0] * 26
        for letter_count in letter_counts:
            for c in range(26):
                total_letter_count[c] += letter_count[c]
        #for c in range(26):
        #    total_letter_count[c] /= float(sum(total_letter_count))
        yield int(year), total_letter_count
        
    def steps(self):
        return [self.mr(mapper=self.letter_frequencies, 
                        reducer=self.sum_frequencies),]

if __name__ == '__main__':
    ScrabbleLetterCounter.run()