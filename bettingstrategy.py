# Models a betting strategy for soccer:

class Bet:
    """ Represents a bet on an outcome (win/lose) and calculates the amounts
        on win/lose. """
    def __init__(self, amount, odds):
        self._amount = amount
        self._odds = odds

    def amount(self):
        return self._amount

    def win(self):
        """ Returns the amount won. """
        return self._amount * self._odds - self._amount

    def lose(self):
        """ Returns the amount lost. """
        return self._amount


class Stats:
    """ Statistics calculated from evaluating a betting strategy. """
    def __init__(self):
        self._number_wins = self._number_busts = 0
        self._gains = self._losses = 0
        self._profits = 0

    def __str__(self):
        return "profit {} gains {} losses {} #wins {} #losses {}".format(
                self._profits, self._gains, self._losses, self._number_wins,
                self._number_busts)


class BettingStrategy:
    """ Base class for different types of betting strategies. Allows for
        easy comparison between different strategies. """

    def calc_stats(amount_per_bet, season_data):
        """ Returns a stats object. """
        return Stats()

    def strategy_name(season_data):
        return "BaseStrategy"
