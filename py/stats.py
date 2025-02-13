from settings import *

class Stats:
    def __init__(self, health, damage, speed, range = 0, gold_dropped = None, upgrades = None):
        ## Player Stats ##
        self.base_stats = {
            'Health' : health,
            'Damage' : damage,
            'Speed' : speed,
            'Range' : range,
        }

        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range

        ## Enemy Stats ##
        self.gold_dropped = gold_dropped

        if upgrades:
            self.upgrades = upgrades
            self.applyUpgrades()
    
    def applyUpgrades(self):
        for key, count in self.upgrades.upgrade_count.items():
             if count > 0:
                setattr(self,
                        key.lower(), 
                        self.base_stats[key] + self.upgrades.on_upgrade[key] * count
                    )


    def copyEnemy(self):
        return Stats(self.health, self.damage, self.speed, gold_dropped = self.gold_dropped)
    
    def copyPlayer(self):
        return Stats(self.health, self.damage, self.speed, self.range, upgrades = self.upgrades)

class Upgrades:
    def __init__(self):
        self.upgrade_costs = {
            'Health' : 100,
            'Damage' : 150,
            'Speed' : 200,
            'Range' : 300,
        }

        self.on_upgrade = {
            'Health' : 50,
            'Damage' : 25,
            'Speed' : 20,
            'Range' : 30,
        }

        self.upgrade_count = {
            'Health' : 0,
            'Damage' : 0,
            'Speed' : 0,
            'Range' : 0,
        }
    
    def getUpgrades(self):
        return [key for key in self.upgrade_costs.keys()]
    
    def buyUpgrade(self, stat):
        if stat in self.on_upgrade:
            self.upgrade_count[stat] += 1
            self.upgrade_costs[stat] = int(self.upgrade_costs[stat] * 1.2)

        

class Gold:
    def __init__(self):
        self.balance = 900
        self.earned = 0
        self.spent = 0

    def add(self, amount):
        self.balance += amount
