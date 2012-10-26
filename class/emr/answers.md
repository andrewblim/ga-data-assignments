
# Data Class Week 3 Answers

Andrew Lim / 25 Oct 2012

To run the EMR job yourself, run `bash run-emr.sh`, overwriting the output parameter in the script with your own S3 location. It takes several hours with the default mrjob settings, so you'll probably want to add more instances. I downloaded the output from my own run of the script to the `emr_output` directory. To print letter frequencies (with the letter S omitted) and the mean squared errors, run `python convert_frequencies.py`. 

`pip freeze` on my virtualenv: 

    PyYAML==3.10
    Pygments==1.5
    boto==2.6.0
    ipython==0.13
    matplotlib==1.1.1
    mrjob==0.3.5
    nose==1.2.1
    numpy==1.6.2
    pandas==0.9.0
    patsy==0.1.0
    python-dateutil==2.1
    pytz==2012f
    pyzmq==2.2.0.1
    scikit-learn==0.12.1
    scipy==0.11.0
    simplejson==2.6.2
    six==1.2.0
    statsmodels==0.5.0
    tornado==2.4
    wsgiref==0.1.2

### Explanation of project

[According](http://www.scrabble-assoc.com/info/history.html) to the National Scrabble Association, Scrabble inventor Alfred Mosher Butts studied the front pages of the New York Times in order to determine letter frequencies in his game (although Wikipedia [states](http://en.wikipedia.org/wiki/Alfred_Mosher_Butts) he deliberately restricted the number of S tiles). Butts did by hand what modern computers can do programmatically with much greater speed and on much larger sets of data. Google Ngrams offers a large data set of word usage over time; its corpus texts are analogous to the NYT front pages that Butts scoured. 

I used to really enjoy playing Scrabble as a kid, and I've recently taken up Words With Friends. The games are extremely similar, but WWF has some slight variations, including in its letter frequencies. I'd like to use the Ngrams data set to see whether WWF's frequencies are a better match than Scrabble's frequencies to actual American English language use; I think they are. I'd also like to see whether that has changed over time - if during the 1930s, when Scrabble was invented, Scrabble's frequencies were a better fit. I think this is not the case and that WWF will have just a more accurate fit in either case; Butts was going by hand with the NYT, after all. 

I used 1-grams from two date ranges: 1938-1948 (representing the time Scrabble was originally developed) and 2005 onward (representing present-day). I would have loved to do all years but that was very slow to upload to S3 and to run. I reduced the downloaded Ngrams files to these date ranges with `awk '{ if (($2>=1938 && $2<=1948) || $2>=2005) print; }' decompressed_ngrams_file > reduced_ngrams_file`. (I wish Google had posted random subsamples of their Ngrams data, as I've seen done on some large sets; then I could have done more years.)

I used the Ngrams American English data set version 20120701, in part because the NYT represents an American English corpus, but also because the data set was slightly smaller. The word list I used was TWL06, downloaded from the Internet Scrabble Club's [repository of dictionaries](http://www.isc.ro/en/commands/lists.html). TWL06 is the official word list for North American Scrabble tournaments. 

Scrabble tile frequencies were found [here](http://en.wikipedia.org/wiki/Scrabble_letter_distributions). Words with Friends tile frequencies were found [here](http://tile-counter.com/wwf-tile-distribution-and-letter-frequency). 

### File info

All data files can be found at `s3://andrewblim-ngrams/twl06-analysis`, which is public. The Ngrams data are at `s3://andrewblim-ngrams/twl06-analysis/reduced-ngrams/reduced_ngrams_<letter>.gz` and the TWL06 word list is at `s3://andrewblim-ngrams/twl06-analysis/TWL06.txt`. 

### Findings

The percentage frequencies, **excluding the letter S** because their frequencies in the game may not have been intended to reflect true language frequency, and also excluding blank tiles, are below. (And sorry if you are reading this as raw text and not with a Markdown reader.) 

The mean squared errors of the percentages (decimal percentages * 100) were:

- 1938-1948 data vs. 2005- data: 0.005417
- 1938-1948 data
    - vs. Scrabble: 1.863341
    - vs. WWF: 1.791344
- 2005- data:
    - vs. Scrabble: 1.233373
    - vs. WWF: 1.163682

This supports the hypothesis that Words with Friends would be more reflective of English language use in both eras. The difference in letter frequencies between eras is small. WWF makes notable improvements to E, I, H, and T, is better in most letters (it has slightly more tiles which creates small improvements across the board), and is only worse in a few places, notably N. 

<table>
    <tr>
        <th>Letter</th>
        <th>Scrabble</th>
        <th>WWF</th>
        <th>1938-1948</th>
        <th>2005-</th>
    </tr>
    <tr>
        <td>A%</td>
        <td>9.57%</td>
        <td>9.28%</td>
        <td>7.98%</td>
        <td>8.02%</td>
    </tr>
    <tr>
        <td>B%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>1.61%</td>
        <td>1.56%</td>
    </tr>
    <tr>
        <td>C%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>3.42%</td>
        <td>3.35%</td>
    </tr>
    <tr>
        <td>D%</td>
        <td>4.26%</td>
        <td>5.15%</td>
        <td>4.19%</td>
        <td>4.29%</td>
    </tr>
    <tr>
        <td>E%</td>
        <td>12.77%</td>
        <td>13.40%</td>
        <td>13.62%</td>
        <td>13.53%</td>
    </tr>
    <tr>
        <td>F%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>2.73%</td>
        <td>2.54%</td>
    </tr>
    <tr>
        <td>G%</td>
        <td>3.19%</td>
        <td>3.09%</td>
        <td>2.00%</td>
        <td>2.12%</td>
    </tr>
    <tr>
        <td>H%</td>
        <td>2.13%</td>
        <td>4.12%</td>
        <td>5.75%</td>
        <td>5.73%</td>
    </tr>
    <tr>
        <td>I%</td>
        <td>9.57%</td>
        <td>8.25%</td>
        <td>7.79%</td>
        <td>7.72%</td>
    </tr>
    <tr>
        <td>J%</td>
        <td>1.06%</td>
        <td>1.03%</td>
        <td>0.13%</td>
        <td>0.15%</td>
    </tr>
    <tr>
        <td>K%</td>
        <td>1.06%</td>
        <td>1.03%</td>
        <td>0.56%</td>
        <td>0.68%</td>
    </tr>
    <tr>
        <td>L%</td>
        <td>4.26%</td>
        <td>4.12%</td>
        <td>4.32%</td>
        <td>4.34%</td>
    </tr>
    <tr>
        <td>M%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>2.61%</td>
        <td>2.64%</td>
    </tr>
    <tr>
        <td>N%</td>
        <td>6.38%</td>
        <td>5.15%</td>
        <td>7.63%</td>
        <td>7.65%</td>
    </tr>
    <tr>
        <td>O%</td>
        <td>8.51%</td>
        <td>8.25%</td>
        <td>8.33%</td>
        <td>8.36%</td>
    </tr>
    <tr>
        <td>P%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>2.25%</td>
        <td>2.22%</td>
    </tr>
    <tr>
        <td>Q%</td>
        <td>1.06%</td>
        <td>1.03%</td>
        <td>0.12%</td>
        <td>0.12%</td>
    </tr>
    <tr>
        <td>R%</td>
        <td>6.38%</td>
        <td>6.19%</td>
        <td>6.68%</td>
        <td>6.58%</td>
    </tr>
    <tr>
        <td>T%</td>
        <td>6.38%</td>
        <td>7.22%</td>
        <td>10.21%</td>
        <td>10.13%</td>
    </tr>
    <tr>
        <td>U%</td>
        <td>4.26%</td>
        <td>4.12%</td>
        <td>2.92%</td>
        <td>2.98%</td>
    </tr>
    <tr>
        <td>V%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>1.07%</td>
        <td>1.10%</td>
    </tr>
    <tr>
        <td>W%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>1.93%</td>
        <td>2.00%</td>
    </tr>
    <tr>
        <td>X%</td>
        <td>1.06%</td>
        <td>1.03%</td>
        <td>0.22%</td>
        <td>0.22%</td>
    </tr>
    <tr>
        <td>Y%</td>
        <td>2.13%</td>
        <td>2.06%</td>
        <td>1.81%</td>
        <td>1.90%</td>
    </tr>
    <tr>
        <td>Z%</td>
        <td>1.06%</td>
        <td>1.03%</td>
        <td>0.08%</td>
        <td>0.08%</td>
    </tr>
</table>