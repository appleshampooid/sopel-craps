from sopel import module
import re
import requests
from .game import CrapsGame

def setup(bot):
    bot.memory['craps'] = CrapsGame()

@module.rule('(\d+) on the (pass) line')
@module.rule('(\d+) (come)')
def bet(bot, trigger):
    """"""
    craps = bot.memory['craps']
    # if not trigger.group(3):
    #     bot.say("Got to put some chips on the table to play!")
    #     return
    # amount = None
    # try:
    #     amount = int(trigger.group(3))
    # except ValueError:
    #     bot.say("Chips must be integer-like, gosh")
    #     return
    # if bet_type in BetType.__members__:
    amount = int(trigger.group(1))
    craps.bet(trigger.nick, trigger.group(2).lower(), amount)
    # else:
    #     bot.say("Sorry, we don't take that kind of bet at this table.")

@module.rule('(\d+) odds( on the (\d+))?')
def odds(bot, trigger):
    # bot.say("groups 1 2 3 are: {} {} {}".format(trigger.group(1),trigger.group(2),trigger.group(3)))
    craps = bot.memory['craps']
    amount = int(trigger.group(1))
    player_bets = filter(lambda b: b.player.nick == trigger.nick , craps.bets)
    if trigger.group(2):
        number = int(trigger.group(3))
    else:
        number = craps.point
    found = False
    for b in player_bets:
        if b.number == number:
            b.add_odds(amount)
            found = True
    if not found:
        bot.say("You don't have a bet on the {}!".format(number))
    
@module.commands('bets')
def bets(bot, trigger):
    craps = bot.memory['craps']
    bets = filter(lambda b: b.player.nick == trigger.nick , craps.bets)
    for b in bets:
        bot.say('{}, you have a {}'.format(trigger.nick, b.to_string()))

@module.commands('shoot')
def shoot(bot, trigger):
    craps  = bot.memory['craps']
    craps.roll(bot)

@module.commands('table')
def table(bot, trigger):
    craps  = bot.memory['craps']
    craps.table(bot)

@module.commands('chips')
def chips(bot, trigger):
    craps = bot.memory['craps']
    if trigger.nick in craps.players:
        bot.say('{}, you have {} in chips.'.format(trigger.nick, craps.players[trigger.nick].bank))
