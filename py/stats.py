from settings import *

class Stats:
    def __init__(self, health, damage, speed, range = 0):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range

    def copy(self):
        return Stats(self.health, self.damage, self.speed, self.range)
    
    def upgrades(self):
        ## TODO i think make upgrades go through this and return new stats?? maybe ##
        pass

class Upgrades:
    def __init__(self):
        pass

class Gold:
    def __init__(self):
        self.balance = 0
        self.earned = 0
        self.spent = 0

    def add(self, amount):
        self.balance += amount
