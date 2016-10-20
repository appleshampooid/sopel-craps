from enum import Enum
import random
from .bets import *

class CrapsGame:
    def __init__(self, bot):
        self.players = {}
        self.bot = bot
        self.point = None
        self.bets = []

    def table(self, bot):
        if self.point:
            bot.say("The point is {}.".format(self.point))
        else:
            bot.say("The point is OFF.")
        
    def bet(self, nick, amount):
        if not nick in self.players:
            self.players[nick] = Player(nick)
        self.bets.append(PassLineBet(amount, self.players[nick]))
        self.players[nick].bank -= amount
            
    def roll(self, bot):
        roll = Roll()
        bot.say("Roll is {}+{} = {}".format(roll.n1, roll.n2, roll.total))
        new_bets = []
        for bet in self.bets:
            if bet.eval(bot, self, roll):
                new_bets.append(bet)
        self.bets = new_bets
            
        if self.point:
            if roll.total == 7 or roll.total == self.point:
                self.point = None
        else:
            if roll.is_point():
                self.point = roll.total

class Player:
    def __init__(self, nick):
        self.nick = nick
        self.bank = 10000.0

class Roll:
    def __init__(self):
        self.n1 = random.randint(1, 6)
        self.n2 = random.randint(1, 6)
        self.total = self.n1 + self.n2

    def is_point(self):
        return self.total in (4, 5, 6, 8, 9, 10)

    def is_crap(self):
        return self.total in (2, 3, 12)

