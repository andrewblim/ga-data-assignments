
from pylab import *
import itertools
import pandas as pd
import random as pyrandom  # since pylab uses 'random'

# problem 1: coin toss

def coin_toss(n, csv_filename=None, hist_filename=None):
    levels = ['H', 'T']
    tosses = pd.Series([levels[x] for x in randint(0, 2, size=n)], name='tosses')
    if csv_filename is not None:
        tosses.to_csv(csv_filename, header=True, index=False)
    if hist_filename is not None:
        x = arange(2)
        counts = [sum(tosses == level) for level in levels]
        bar(x, counts, width=1)
        xlim(0, 2)
        xticks(x + 0.5, ['heads', 'tails'])
        savefig(hist_filename)
        close()
    return tosses

# problem 2 and 3: dice toss

def dice_toss(num_dice, n, csv_filename=None, hist_filename=None):
    rolls = pd.DataFrame(index=arange(n))
    for die in range(num_dice):
        label = 'die' + str(die)
        rolls[label] = pd.Series(randint(1, 7, size=n))
    if csv_filename is not None:
        rolls.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        x = arange(num_dice, num_dice * 6 + 1)
        totals = [sum(rolls.ix[i]) for i in rolls.index]
        counts = [sum(totals == total) for total in x]
        bar(x, counts, width=1)
        xlim(min(x), max(x) + 1)
        xticks(x + 0.5, x)
        savefig(hist_filename)
        close()
    return rolls

# helper classes for problems 4 and 5

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __str__(self):
        ranks = ['A'] + map(str, range(2, 10)) + ['T', 'J', 'Q', 'K']
        suits = ['C', 'D', 'H', 'S']
        return ranks[self.rank] + suits[self.suit]
    def __repr__(self):
        return '<Card %s>' % self.__str__()
    @property
    def value(self):
        return self.suit * 13 + self.rank

class Deck:
    def __init__(self):
        self.cards = {}
        for rank_suit in zip(sorted(range(13) * 4), range(4) * 13):
            self.cards[rank_suit] = Card(*rank_suit)
    def draw(self, n):
        return pyrandom.sample(self.cards.values(), n)
    @property
    def sorted_cards(self):
        return sorted(self.cards.values(), key=lambda x: x.value)

# problem 4, and also called in problem 5: card draw

def card_draw(num_cards, n, deck, csv_filename=None, hist_filename=None):
    draws = pd.DataFrame(index=arange(n),
                         columns=['card' + str(i) for i in range(num_cards)])
    for i in draws.index:
        draws.ix[i] = deck.draw(num_cards)
    if csv_filename is not None:
        draws.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        x = arange(52)
        counts = [0] * 52
        for col in draws.columns:
            for i in draws.index:
                card = draws[col][i]
                counts[card.value] += 1
        barcolor = sorted(['b'] * 13 + ['y'] * 13 + ['r'] * 13 + ['g'] * 13)
        bar(x, counts, width=1, color=barcolor)
        xlim(0, 52)
        xticks(arange(4) * 13 + 6.5, ['clubs A-K', 'diamonds A-K', 'hearts A-K', 'spades A-K'])
        savefig(hist_filename)
        close()
    return draws

# helper functions for problem 5 - strength of poker hands

def is_straight_flush(hand):
    if is_flush(hand) and is_straight(hand): return True
    else: return False

def is_quads(hand):
    return is_k_of_a_kind(hand, 4)

def is_full_house(hand):
    ranked_hand = sorted(hand, key=lambda card: card.rank)
    if is_trips(ranked_hand[0:3]) and is_pair(ranked_hand[3:5]):
        return True
    elif is_trips(ranked_hand[2:5]) and is_pair(ranked_hand[0:2]):
        return True
    else:
        return False

def is_flush(hand):
    if len(set([card.suit for card in hand])) == 1: return True
    else: return False

def is_straight(hand):
    ranks = sorted([card.rank for card in hand])
    if len(set(ranks)) == len(ranks): 
        if ranks[len(ranks)-1] - ranks[0] == len(ranks)-1:
            return True
        elif ranks[0] == 0 and ranks[len(ranks)-1] - ranks[1] == len(ranks)-2:
            return True  # ace-high
    else:
        return False

def is_trips(hand):
    return is_k_of_a_kind(hand, 3)

def is_two_pair(hand):
    ranked_hand = sorted(hand, key=lambda card: card.rank)
    for i in range(2, len(ranked_hand)-1):
        if is_k_of_a_kind(ranked_hand[:i], 2) and is_k_of_a_kind(ranked_hand[i:], 2):
            return True
    return False

def is_pair(hand):
    return is_k_of_a_kind(hand, 2)

def is_k_of_a_kind(hand, k):
    ranks = sorted([card.rank for card in hand])
    for i in range(len(ranks) - k + 1):
        if len(set(ranks[i:i+k])) == 1:
            return True
    return False

# problem 5 - poker draws

def poker_draw(n, deck, csv_filename=None, hist_filename=None):
    draws = card_draw(5, n, deck, None, None)
    hands = []
    for i in draws.index:
        hand = draws.ix[i]
        if is_straight_flush(hand):
            hands.append('straight flush')
        elif is_quads(hand):
            hands.append('four of a kind')
        elif is_full_house(hand):
            hands.append('full house')
        elif is_flush(hand):
            hands.append('flush')
        elif is_straight(hand):
            hands.append('straight')
        elif is_trips(hand):
            hands.append('three of a kind')
        elif is_two_pair(hand):
            hands.append('two pairs')
        elif is_pair(hand):
            hands.append('pair')
        else:
            hands.append('high card')
    draws['hand'] = hands
    if csv_filename is not None:
        draws.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        x = arange(9)
        levels = ['high card', 'pair', 'two pairs', 'three of a kind', 
                  'straight', 'flush', 'full house', 'four of a kind',
                  'straight flush']
        labels = ['hi card', 'pair', '2 pair', 'trips', 'straight', 
                  'flush', 'full house', 'quads', 'st. flush']
        counts = [0] * 9
        for i in draws.index:
            counts[levels.index(draws['hand'][i])] += 1
        bar(x, counts, width=1)
        tick_params(labelsize='x-small')
        xticks(x + 0.5, labels)
        xlim(0, 9)
        savefig(hist_filename)
        close()
    return draws

# problem 6 - roulette wheel

def roulette_spin(n, csv_filename=None, hist_filename=None):
    levels = range(37) + ['00']
    spins = pd.Series([levels[x] for x in randint(0, len(levels), size=n)], name='spins')
    if csv_filename is not None:
        spins.to_csv(csv_filename, header=True, index=False)
    if hist_filename is not None:
        x = arange(len(levels))
        counts = [sum(spins == level) for level in levels]
        bar(x, counts, width=1)
        xlim(0, len(levels))
        tick_params(labelsize='x-small')
        xticks(x + 0.5, levels)
        savefig(hist_filename)
        close()
    return spins

# problem 7 - roulette wheel to bankruptcy, betting on black

def roulette_to_bankruptcy(initial_bank, n, csv_filename=None, hist_filename=None):
    runs = pd.Series(index=arange(n), name='runs', dtype=int)
    for i in runs.index:
        bank = initial_bank
        run_length = 0
        while bank > 0:
            run_length += 1
            spin = randint(0,38)
            if spin < 18: bank += 1
            else: bank -= 1
        runs.ix[i] = run_length
    if csv_filename is not None:
        runs.to_csv(csv_filename, header=True, index=False)
    if hist_filename is not None:
        hist(runs, bins=20)
        savefig(hist_filename)
        close()
    return runs

# problem 8 - elevator weight limit
# approximating weight with a normal distribution

def elevator_weight(num_people, limit, n, mean_weight, sd_weight, 
                    csv_filename=None, hist_filename=None):
    runs = pd.DataFrame(index=arange(n))
    for i in range(num_people):
        label = 'person' + str(i)
        runs[label] = normal(mean_weight, sd_weight, n)
    runs['sum'] = runs.apply(sum, axis=1)
    runs['overweight'] = runs['sum'] > limit
    if csv_filename is not None:
        runs.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        bin_start = floor(min(runs['sum']))
        bin_end = ceil(max(runs['sum'])) + 1
        bin_width = (bin_end - bin_start) / 30.0
        bins = arange(bin_start, bin_end, bin_width)
        hist(runs['sum'], bins=bins, color='b', label='All sums')
        tail_values = filter(lambda x: x >= limit, runs['sum'])
        hist(tail_values, bins=bins, color='r', label='Sums over limit')
        legend(prop={'size': 'small'})
        savefig(hist_filename)
        close()
    return runs

# problem 9 - website visits

def website_visits(visit_rate, purchase_rate, start_date, n, csv_filename=None, 
                   hist_filename=None):
    obs = pd.DataFrame(index=arange(n))
    obs['dates'] = pd.date_range(start_date, periods=n, freq='d')
    obs['visits'] = np.random.poisson(visit_rate, size=n)
    obs['purchases'] = map(lambda x: np.random.binomial(x, purchase_rate), obs['visits'])
    if csv_filename is not None:
        obs.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        subplot(221)
        tick_params(labelsize='x-small')
        hist(obs['visits'], bins=20, color='b', label='Visits')
        legend(prop={'size': 'small'})
        subplot(222)
        tick_params(labelsize='x-small')
        hist(obs['purchases'], bins=20, color='g', label='Purchases')
        legend(prop={'size': 'small'})
        subplot(212)
        tick_params(labelsize='x-small')
        scatter(obs['visits'], obs['purchases'])
        xlabel('visits')
        ylabel('purchases')
        savefig(hist_filename)
        close()
    return obs

# problem 10 - stock prices

def stock_prices(drift, volatility, initial_price, n, csv_filename=None, 
                 hist_filename=None):
    obs = pd.DataFrame(index=arange(n))
    obs['returns'] = np.random.normal(drift/252, volatility/sqrt(252), n)  # 252 = annualization factor
    prices = [0] * n
    prices[0] = initial_price * (1 + obs.ix[0]['returns'])
    for i in range(1, n):
        prices[i] = prices[i-1] * (1 + obs.ix[i]['returns'])
    obs['prices'] = prices
    if csv_filename is not None:
        obs.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        subplot(221)
        tick_params(labelsize='x-small')
        hist(obs['returns'], bins=20, color='b', label='Returns')
        legend(prop={'size': 'x-small'})
        subplot(222)
        tick_params(labelsize='x-small')
        hist(obs['prices'], bins=20, color='g', label='Prices')
        legend(prop={'size': 'x-small'})
        subplot(212)
        tick_params(labelsize='x-small')
        plot(range(n), obs['prices'])
        xlabel('time')
        ylabel('price')
        savefig(hist_filename)
        close()
    return obs
        
# problem 11 - bank cash flows
# A simple example - loan starts are Poisson distributed and are all the same 
# size, same tenor, pay the same rate of interest, and have the same probability 
# of default at each time period. Loans of each vintage are kept track of with a 
# queue; pass print_loan_queue=True to see the loan queue at each point in time. 

def bank_flows(loan_freq, loan_size, tenor, interest_rate, default_prob, n, 
               csv_filename=None, hist_filename=None, print_loan_queue=False):
    
    obs = pd.DataFrame(index=arange(n))
    obs['loans_made'] = np.random.poisson(loan_freq, n)
    obs['loans'] = -obs['loans_made'] * loan_size
    
    loans_out = [0] * tenor
    interest = [0] * n
    principal = [0] * n
    
    for i in obs.index:
        # randomly default some loans, then pay interest and principal
        if print_loan_queue:
            print i, loans_out
        loans_out = map(lambda x: np.random.binomial(x, 1-default_prob) if x > 0 else 0, loans_out)
        interest[i] = sum(loans_out) * loan_size * interest_rate
        principal[i] = loans_out.pop() * loan_size
        loans_out.insert(0, obs['loans_made'][i])
    obs['interest'] = interest
    obs['principal'] = principal
    
    obs['cash_flow'] = obs['loans'] + obs['interest'] + obs['principal']
    obs['cumulative_cash_flow'] = np.cumsum(obs['cash_flow'])
    
    if csv_filename is not None:
        obs.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        subplot(211)
        tick_params(labelsize='x-small')
        hist(obs['cash_flow'], bins=20, color='b', label='Cash flow')
        legend(prop={'size': 'x-small'})
        subplot(212)
        tick_params(labelsize='x-small')
        plot(range(n), obs['cumulative_cash_flow'])
        xlabel('time')
        ylabel('cumulative cash flow')
        savefig(hist_filename)
        close()
    
    return obs

# problem 12 - custom - baseball runs
# Sports stats are a side interest of mine. Calculate runs scored in an inning
# of baseball given a very simplified model of a baseball game where you supply
# the following parameters:
#  - prob of single, double, triple, and HR - all else considered strikeouts
#  - all runners advance the same # of bases as the hit
# Hit probabilities supplied as a list [single, double, triple, HR] i.e.
# [0.250, 0.050, 0.005, 0.050]

def baseball_runs(prob_hits, n, csv_filename=None, hist_filename=None):
    obs = pd.DataFrame(index=arange(n))
    prob_hits_rev = prob_hits
    prob_hits_rev.reverse()
    prob_stack = np.cumsum(list(prob_hits_rev))
    obs['runs'] = [0] * n
    obs['batters_faced'] = [0] * n
    for i in obs.index:
        runs = 0
        outs = 0
        batters_faced = 0
        bases = [0, 0, 0]
        while outs < 3:
            event = np.random.uniform(0, 1)
            if event < prob_stack[3]: # at least a single
                runs += bases.pop()
                bases.insert(0, 1)  
                if event < prob_stack[2]: # at least a double
                    runs += bases.pop()
                    bases.insert(0, 0)
                if event < prob_stack[1]: # at least a triple
                    runs += bases.pop()
                    bases.insert(0, 0)
                if event < prob_stack[0]: # home run
                    runs += bases.pop()
                    bases.insert(0, 0)
            else: # an out
                outs += 1
            batters_faced += 1
        obs['runs'][i] = runs
        obs['batters_faced'][i] = batters_faced
    if csv_filename is not None:
        obs.to_csv(csv_filename, index=False)
    if hist_filename is not None:
        subplot(211)
        tick_params(labelsize='x-small')
        hist(obs['runs'], color='g', label='Runs', bins=arange(max(obs['runs'])))
        legend(prop={'size': 'x-small'})
        subplot(212)
        tick_params(labelsize='x-small')
        hist(obs['batters_faced'], color='r', label='Batters faced', 
             bins=arange(max(obs['batters_faced'])))
        legend(prop={'size': 'x-small'})
        savefig(hist_filename)
        close()
    return obs
