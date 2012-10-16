
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
        x = arange(0, 2)
        counts = [sum(tosses == level) for level in levels]
        bar(x, counts, width=1)
        xlim(0, 2)
        xticks(x + 0.5, levels)
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
    if isFlush(hand) and isStraight(hand): return True
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

def roulette_spin(n, ):

if __name__ == '__main__':
    n = 1000
    #coin_toss(n, 'coin_toss.csv', 'coin_toss.png')
    #dice_toss(1, n, 'die_toss.csv', 'die_toss.png')
    #dice_toss(2, n, 'dice_toss.csv', 'dice_toss.png')
    #card_draw(1, n, Deck(), 'card_draw.csv', 'card_draw.png')
    #poker_draw(n, Deck(), 'poker_draw.csv', 'poker_draw.png')