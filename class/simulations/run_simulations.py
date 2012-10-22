from simulations import *

if __name__ == '__main__':
    
    n = 1000
    
    coin_toss(n, 'coin_toss.csv', 'coin_toss.png')
    print('Coin toss written to coin_toss.csv, coin_toss.png')
    
    dice_toss(1, n, 'die_toss.csv', 'die_toss.png')
    print('Die toss written to die_toss.csv, die_toss.png')
    dice_toss(2, n, 'dice_toss.csv', 'dice_toss.png')
    print('2-dice toss written to dice_toss.csv, dice_toss.png')
    
    card_draw(1, n, Deck(), 'card_draw.csv', 'card_draw.png')
    print('Card draw written to card_draw.csv, card_draw.png')
    poker_draw(n, Deck(), 'poker_draw.csv', 'poker_draw.png')
    print('Poker draw written to poker_draw.csv, poker_draw.png')
    
    roulette_spin(n, 'roulette_spin.csv', 'roulette_spin.png')
    print('Roulette spin written to roulette_spin.csv, roulette_spin.png')
    roulette_to_bankruptcy(25, n, 'roulette_to_bankruptcy.csv', 'roulette_to_bankruptcy.png')
    print('Roulette-to-bankruptcy spin written to roulette_to_bankruptcy.csv, roulette_to_bankruptcy.png')
    
    elevator_weight(10, 1750, n, 160, 40, 'elevator_weight.csv', 'elevator_weight.png')
    print('Elevator weight written to elevator_weight.csv, elevator_weight.png')
    
    website_visits(500, 0.05, '1/1/2010', n, 'website_visits.csv', 'website_visits.png')
    print('Website visits written to website_visits.csv, website_visits.png')
    stock_prices(0.03, 0.3, 100, n, 'stock_prices.csv', 'stock_prices.png')
    print('Stock prices written to stock_prices.csv, stock_prices.png')
    bank_flows(100, 100, 5, 0.05, 0.04, n, 'bank_flows.csv', 'bank_flows.png')
    print('Bank flows written to bank_flows.csv, bank_flows.png')
    
    baseball_runs([0.275, 0.075, 0.005, 0.04], n, 'baseball_runs.csv', 'baseball_runs.png')
    print('Baseball runs (custom exercise) written to baseball_runs.csv, baseball_runs.png')