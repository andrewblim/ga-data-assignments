
# Data Class Week 1 Answers

Andrew Lim
17 Oct 2012

To run everything, run `python run_simulations.py`. 

`pip freeze` on my virtualenv: 

    Pygments==1.5
    ipython==0.13
    matplotlib==1.1.1
    nose==1.2.1
    numpy==1.6.2
    pandas==0.9.0
    patsy==0.1.0
    python-dateutil==2.1
    pytz==2012f
    pyzmq==2.2.0.1
    scikit-learn==0.12.1
    scipy==0.11.0
    six==1.2.0
    statsmodels==0.5.0
    tornado==2.4
    wsgiref==0.1.2

### Problems

1. (`coin_toss.csv` and `coin_toss.png`) This is a binary(0.5) distributed variable. 

2. (`die_toss.csv` and `die_toss.png`) This has a pmf of f(x) = 1/6 for x in {1,2,3,4,5,6}. 

3. (`dice_toss.csv` and `dice_toss.png`) This has a pmf of f(x) = (6-|7-x|) * (1/6)^2 for x an integer in [2-12]. 

4. (`card_draw.csv` and `card_draw.png`) Each card is equally likely to turn up, so this just has a pmf of f(c) = 1/52 for c in the set of 52 possible playing cards. 

5. (`poker_draw.csv` and `poker_draw.png`) There are 52 choose 5 = 2598960 possible poker hands. The easiest way to calculate the probability of each hand is to calculate the number of ways that hand can be achieved and divide by this number. This is all pretty clearly [on Wikipedia](http://en.wikipedia.org/wiki/List_of_poker_hands), but here's the explanation anyway: 

    Straight flush (40 ways): can start A-10 in 4 suits = 4*10
    
    Four of a kind (624): can be all 13 ranks plus one extra card that can be one of 48 = 13 * 48
    
    Full house (3744): 13 ranks for the 3 * 12 ranks for the 2, and then for each rank combination there are 4 ways to do the 3 and 6 ways to do the 2. So 13 * 12 * 4 * 3
    
    Flush (5108): 13 choose 5 flushes = 1287, times 4 suits, then subtract 40 for the straight flushes
    
    Straight (10200): can start A-10 and each such straight has 4^5 ways that can be made, because each card can be any suit. So 10 * 4^5, then subtract 40 for the straight flushes. 
    
    Three of a kind (54912): can be in any of the 13 ranks. There are four ways among the suits to make three of a kind. There are 48 possibilities for the 4th card that would not make it four of a kind, and 44 possibilities for the fifth card that would not make it a full house, and then we have to divide by 2 since 48 * 44 would double count everything (if we had AAA, then it would count both 23 and 32 as options). So 13 * 4 * 48 * 44 / 2. 
    
    Two pair (123552): 13 choose 2 possible rank combinations = 78, within each rank combination there are 6 ways to make each pair among the 4 suits, and the fifth card can be one of 44. So 78 * 6 * 6 * 44. 
    
    Pair (1098240): 13 possible ranks, 6 ways to make each rank pair. Then there are 48 possibilities for card 3, 44 for card 4, and 40 for card 5, but then we divide by 6 because we've counted 6 times extra on cards 3-5 (6 = 3!; by example, if we had AA we've counted 234, 243, 324, 342, 423, and 432 all distinctly). So 13 * 6 * 48 * 44 * 40 / 6. 
    
    High card (1302540): everything else. 

6. (`roulette_spin.csv` and `roulette_spin.png`) Each slot is equally likely to turn up, so this has a pmf of f(s) = 1/38 for s in the set of 38 possible slots (1-36, 0, and 00). 

7. (`roulette_to_bankruptcy.csv` and `roulette_to_bankruptcy.png`) Each roll has a 18/38 chance of success (black) and a 20/38 chance of failure (red, or the 0 or 00). This variable is the expected number of rolls before we see 25 more failures than successes. I couldn't get a closed-form pdf out of this one, it was kind of sticky. 

8. (`elevator_weight.csv` and `elevator_weight.png`) I represented each weight as a normally distributed variable with mean 160lbs and standard deviation 40lbs. Normal isn't going to be the exact right distribution; you can have negative values, (although they are very unlikely with that parameterization), plus I imagine there's a little skew, but I don't think it's a bad approximation. The sum of 10 of these is itself normal with mean 1600 and standard deviation 40/sqrt(10), or about 12.6. The probability of being over 1750, the limit I used, is just 1 - N(1750), where N is the normal cdf with that mean and standard deviation. 

9. (`website_visits.csv` and `website_visits.png`) I represented website visits as Poisson events, the distribution that models the events occurring in a time interval if the events are independent of one another. Then I simply modeled the probability of a purchase as a binary variable. 

10. (`stock_prices.csv` and `stock_prices.png`) This is similar to what I used to do for work - I modeled the stock returns using one of the simplest reasonable stock price evolution models, where the returns are normally distributed with a constant mean and standard deviation (hence the stock price itself is lognormal). 

11. (`bank_flows.csv` and `bank_flows.png`) I modeled the number of new loans per period as Poisson, assumed they were all the same size and tenor, and applied a probability of each one defaulting for each period - so a loan with default parameter p would have probability p of defaulting in period 1, (1-p) * p in period 2, (1-p)^2 * p, etc. and of course might not default at all (the bank hopes). This makes it like a geometric variable, though the upper tail is capped at the duration of the loan. For each period where a loan is not defaulted it pays a fixed interest, and if it survives it pays principal at maturity. With the parameters used in `run_parameters.py` you get a steady upward flow after an initial negative outlay of cash for the first several loans, although if you make the default parameter higher you can change that. 

12. (`baseball_runs.csv` and `baseball_runs.png`) I'm a baseball fan and more generally a fan of statistical analysis in sports, so I made a simple model of baseball run-scoring and batters faced by inning. The batters faced has a negative binomial distribution with probability parameter = Pr(not getting out), which in my model is equal to Pr(single) + Pr(double) + Pr(triple) + Pr(home run). The run distribution is similar but a little more complicated because the type of hit varies and runners occupy intermediate bases before scoring and can get left there. I read a paper some years back (Steven Miller, [A derivation of the Pythagorean won-loss formula in baseball](http://arxiv.org/pdf/math/0509698v4.pdf)) showing that it had some similarities to the Weibull distribution. My model is likely to underestimate because it doesn't take into account runners advancing extra bases on hits and runners advancing on outs. 
