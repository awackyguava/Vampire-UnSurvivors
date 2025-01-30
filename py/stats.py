from settings import *

class Stats:
    def __init__(self, health, damage, speed, range = 0, gold_dropped = 0):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range

        ## Enemy Stats ##
        self.gold_dropped = gold_dropped

    def copyEnemy(self):
        return Stats(self.health, self.damage, self.speed, gold_dropped = self.gold_dropped)
    
    def copyPlayer(self):
        return Stats(self.health, self.damage, self.speed, self.range)
    
    def upgrades(self):
        ## TODO make upgrades go through Upgrades and return new stats?? maybe ##
        pass

class Upgrades:
    def __init__(self):
        self.upgrade_costs = {
            'Health' : 100,
            'Damage' : 150,
            'Speed' : 200,
            'Range' : 300,
            'bb' : 1,
            'test' : 2,
            'e' : 100,
            'er' : 150,
            'erg' : 200,
            'ergh' : 300,
            'erghf' : 1,
            'erghft' : 2,
        }

        self.on_upgrade = {
            'Health' : 50,
            'Damage' : 25,
            'Speed' : 20,
            'Range' : 30,
        }


    
    def getUpgradeCosts(self):
        return [key for key in self.upgrade_costs.keys()]
    
    def buyUpgrade(self, key):
        if key in self.on_upgrade:
            self.stats.key += self.on_upgrade[key]

        

class Gold:
    def __init__(self):
        self.balance = 0
        self.earned = 0
        self.spent = 0

    def add(self, amount):
        self.balance += amount
