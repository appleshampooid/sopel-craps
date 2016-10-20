#!/usr/bin/python3

import unittest
from craps import CrapsGame
from collections import deque

class NotRandom:
    def __init__(self, sequence):
        self.nums = deque(sequence)

    def randint(self, x, y):
        return self.nums.popleft()

class FakeSopel:
    def say(self, msg):
        print(msg)

class CrapsTest(unittest.TestCase):
    def setUp(self):
        self.bot = FakeSopel()
        
    def test_win(self):
        d = CrapsGame(randclass=NotRandom([2,3,2,3]))
        d.bet("foobar", 'pass', 10)
        d.roll(self.bot)
        d.roll(self.bot)
        self.assertEqual(d.players['foobar'].bank,10000+10)

    def test_lose(self):
        c = CrapsGame(randclass=NotRandom([2,3,4,3]))
        c.bet("foobar", 'pass', 10)
        c.roll(self.bot)
        c.roll(self.bot)
        self.assertEqual(c.players['foobar'].bank,10000-10)

if __name__ == '__main__':
    unittest.main()

