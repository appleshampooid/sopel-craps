VALID_BETS=['pass','come']

def get_bet(game, bet_type, amount, player):
    if bet_type == 'pass':
        if game.point:
            return None
        else:
            return Pass(amount, player)
    elif bet_type == 'come':
        if game.point:
            return Come(amount, player)
        else:
            return None

class Bet:
    def __init__(self, amount, player):
        self.amount = amount
        self.player = player

    def odds_win(self, odds):
        if self.number in (6, 8):
            return odds * (6/5)
        elif self.number in (5, 9):
            return odds * (3/2)
        elif self.number in (4, 10):
            return odds * 2
        else:
            raise ValueError("odds_win makes no sense when the bet isn't on a point number!")


class LineBet(Bet):
    def __init__(self, amount, player):
        super().__init__(amount, player)
        self.number = None
        self.odds = 0

    def add_odds(self, odds):
        self.odds = odds
        self.player.bank -= odds

    def eval(self, bot, craps, roll):
        if self.number:
            if roll.total == self.number:
                msg = '{}, you won your {} bet of {}'.format(self.player.nick, self.type(), self.amount)
                odds_win = 0
                if self.odds != 0:
                    odds_win = self.odds_win(self.odds)
                    msg += ' and your odds of {} won {}'.format(self.odds, odds_win)
                bot.say('{}!'.format(msg))
                self.player.bank += self.amount * 2 + self.odds + odds_win
                return False
            elif roll.total == 7:
                msg = '{}, you lost your {} bet of {}'.format(self.player.nick, self.type(), self.amount)
                if self.odds != 0:
                    msg += ' and odds of {}'.format(self.odds)
                bot.say(msg)
                return False
        else:
            if roll.is_point():
                self.number = roll.total
            elif roll.total == 7 or roll.total == 11:
                msg = '{}, you won your {} bet of {}!'.format(self.player.nick, self.type(), self.amount)
                bot.say(msg)
                self.player.bank += self.amount * 2
                return False
            elif roll.is_crap():
                msg = '{}, you lost your {} bet of {}'.format(self.player.nick, self.type(), self.amount)
                bot.say(msg)
                return False
        return True

    def odds_string(self):
        if self.odds:
            return " with odds of {}".format(self.odds)
        else:
            return ''


class Pass(LineBet):
    def type(self):
        return "pass line"
    
    def to_string(self):
        point_text = ''
        if self.number:
            point_text = 'point is {}'.format(self.number)
        else:
            point_text = 'no point'
        return '{} pass line bet ({}){}'.format(self.amount, point_text, self.odds_string())

class Come(LineBet):
    def type(self):
        return "come"

    def to_string(self):
        number_text = ''
        if self.number:
            number_text = 'on the {}'.format(self.number)
        else:
            number_text = "(hasn't traveled)"
        return '{} come bet {}{}'.format(self.amount, number_text, self.odds_string())

