#
# Strategy based on hedging by betting both on a win and lose outcome trying
# to optimize the profit in either case.
#

import bettingstrategy
import dataloader

def _calc_hedging_max_profit(total_bet_amount, odds_home, odds_away):
    """ Returns the 2 best bets (win, lose) from heding home and away 
        team wins. """
    best_win_on_home = best_win_on_away = best_gain = 0

    for amount_on_home in range(0, total_bet_amount+1):
        amount_on_away = total_bet_amount - amount_on_home 
        assert(amount_on_home + amount_on_away == total_bet_amount)

        bet_on_home = bettingstrategy.Bet(amount_on_home, odds_home)
        bet_on_away = bettingstrategy.Bet(amount_on_away, odds_away)

        if min(bet_on_home.win(), bet_on_away.win()) > best_gain:
            best_bet_on_home = bet_on_home
            best_bet_on_away = bet_on_away
            best_gain = min(bet_on_home.win(), bet_on_away.win())
    return best_bet_on_home, best_bet_on_away


class HedgingStrategy(bettingstrategy.BettingStrategy):
    """ Tries to optimize profits by hedging the bet on both winning and 
        losing. """
    def calc_stats(self, amount_per_bet, season_data):
        stats = bettingstrategy.Stats()

        for tup in season_data.iterrows():
            match_data = tup[1]

            # place the bet
            odds_home_win = match_data['B365H']
            odds_away_win = match_data['B365A']
            bet_on_home, bet_on_away = _calc_hedging_max_profit(amount_per_bet,
                odds_home_win, odds_away_win)
    
            outcome = match_data['FTR']
            # draw -> we lose all our money
            if outcome == 'D':
                stats._number_busts = stats._number_busts + 1
                stats._losses = stats._losses + amount_per_bet
            # home win -> win home, lose away
            elif outcome == 'H':
                stats._number_wins = stats._number_wins + 1
                stats._gains = stats._gains + bet_on_home.win()
                stats._losses = stats._losses + bet_on_away.amount()
            # away win -> win away, lose win
            elif outcome == 'A':
                stats._number_wins = stats._number_wins + 1
                stats._gains = stats._gains + bet_on_away.win()
                stats._losses = stats._losses + bet_on_home.amount()
        stats._profits = stats._gains - stats._losses
        return stats

    def strategy_name(self):
        return "Hedging Strategy" 

ds = dataloader.load_country_data_for_league_data_range('be',
        'jupiler_league', 10)

for d in ds:
    hs = HedgingStrategy()
    stats = hs.calc_stats(100, d)
    print(stats)
