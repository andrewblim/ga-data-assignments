import re

nyt_tsvs = ['nyt/arts.tsv',
            'nyt/business.tsv',
            'nyt/obituaries.tsv',
            'nyt/sports.tsv',
            'nyt/world.tsv']

def predict(input_string, categories):
    word_count = {}
    words = clean_text(input_string)
    for word in words:
        if word not in word_count:
            word_count[word] = 1
        else:
            word_count[word] += 1
    for word in word_count:
        # Pr(cat|word) = Pr(word|cat)*Pr(cat)/Pr(word)
        for category in categories:
            pass

def parse_nyt_data(tsvs):
    categories = {}
    for tsv in tsvs:
        categories[tsv] = parse_nyt_tsv(tsv)
    return categories

def parse_nyt_tsv(tsv):
    word_count = {}
    f = open(tsv, 'r')
    for line in f:
        (url, raw_text) = re.split(r'\t', line, maxsplit=1)
        words = clean_text(raw_text)
        for word in words:
            if word == '':
                print raw_text
                print words
                return
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
    return word_count

def clean_text(raw_text):
    # still need to unescape html
    text = re.sub(r'[^\w\s]', r'', raw_text)
    text = re.sub(r'A-Z', r'a-z', text)
    words = re.split(r'\s+', text)
    return words