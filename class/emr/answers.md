
# Data Class Week 3 Answers

Andrew Lim / 25 Oct 2012

To run the EMR job, run `bash run-emr.sh`, overwriting the output parameter in the script with your own S3 location. I downloaded output from my own run to the `emr_output` directory. To convert this to nicely printed letter frequencies with the letter S omitted and get the mean squared errors, run `python convert_frequencies.py`. 

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

I used to really enjoy playing Scrabble as a kid, and I've recently taken up Words With Friends. The games are extremely similar, but WWF has some slight variations, including its letter frequencies. I'd like to use the Ngrams data set to see whether WWF's frequencies are a better match than Scrabble's frequencies to actual American English language use; I think they are. I'd also like to see whether that has changed over time - if during the 1930s, when Scrabble was invented, Scrabble's frequencies were a better fit. I think this is not the case and that WWF will have just a more accurate fit in either case; Butts was going by hand with the NYT, after all. 

I used 1-grams from two date ranges: 1938-1948 (representing the time Scrabble was originally developed) and 2005 onward (representing present-day). I would have loved to do all years but this was very slow both to upload to S3 and to run. I reduced the downloaded Ngrams files to these date ranges with `awk '{ if (($2>=1938 && $2<=1948) || $2>=2005) print; }' decompressed_ngrams_file > reduced_ngrams_file`. 

The huge bottleneck in this project was in fact uploading all of the 1-grams to Amazon S3, which took approximately forever (fine, several hours, but it did make my final submission late, and upload speeds at GA were considerably faster than at my apartment, so I really should have gone there to do this). As mentioned, I did use the Ngrams American English data set version 20120701, in part because the NYT represents an American English corpus, but also because the data set was slightly smaller and I'd be waiting around less. (I wish Google had posted random subsamples as well, as I've seen done on some large data sets; then I could have done more years.)

The word list I used was TWL06, downloaded from the Internet Scrabble Club's [repository of dictionaries](http://www.isc.ro/en/commands/lists.html). TWL06 is the official word list for North American Scrabble tournaments. 

Scrabble tile frequencies were found [here](http://en.wikipedia.org/wiki/Scrabble_letter_distributions). Words with Friends tile frequencies were found [here](http://tile-counter.com/wwf-tile-distribution-and-letter-frequency). 

### File info

All data files can be found at `s3://andrewblim-ngrams/twl06-analysis`, which is public. The Ngrams data are at `s3://andrewblim-ngrams/twl06-analysis/reduced-ngrams/reduced_ngrams_<letter>.gz` and the TWL06 word list is at `s3://andrewblim-ngrams/twl06-analysis/TWL06.txt`. 

### Findings

The percentage frequencies, excluding the letter S because they may not reflect true language frequency in the games, and also excluding blank tiles, are below. (And sorry if you are reading this as raw text and not with a Markdown reader.) 

The mean squared errors of the percentages (decimal percentages * 100) were:

- 1938-1948 data:
    - Scrabble: 
    - WWF: 
- 2005- data:
    - Scrabble: 
    - WWF: 

<table>
    <tr>
        <th>Letter</th>
        <th>Scrabble</th>
        <th>Words With Friends</th>
        <th>Ngrams 1938-1948</th>
        <th>Ngrams 2005-</th>
    </tr>
    <tr>
        <td>A</td>
        <td>9.57</td>
        <td>9.28</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>B</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>C</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>D</td>
        <td>4.26</td>
        <td>5.15</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>E</td>
        <td>12.77</td>
        <td>13.40</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>F</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>G</td>
        <td>3.19</td>
        <td>3.09</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>H</td>
        <td>2.13</td>
        <td>4.12</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>I</td>
        <td>9.57</td>
        <td>8.25</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>J</td>
        <td>1.06</td>
        <td>1.03</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>K</td>
        <td>1.06</td>
        <td>1.03</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>L</td>
        <td>4.26</td>
        <td>4.12</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>M</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>N</td>
        <td>6.38</td>
        <td>5.15</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>O</td>
        <td>8.51</td>
        <td>8.25</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>P</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Q</td>
        <td>1.06</td>
        <td>1.03</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>R</td>
        <td>6.38</td>
        <td>6.19</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>T</td>
        <td>6.38</td>
        <td>7.22</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>U</td>
        <td>4.26</td>
        <td>4.12</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>V</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>W</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>X</td>
        <td>1.06</td>
        <td>1.03</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Y</td>
        <td>2.13</td>
        <td>2.06</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Z</td>
        <td>1.06</td>
        <td>1.03</td>
        <td></td>
        <td></td>
    </tr>
</table>