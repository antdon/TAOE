from importlib.resources import Resource
import time
from incidental import Animal, Tree
from random import random
from constants import *



class Unit():
    def __init__(self, location, health: int) -> None:
        self.prev_location = location
        self.location = location
        self.health = health

    def draw(self, screen):
        screen.addstr(*self.prev_location, " ", curses.color_pair(BLANK_COLOR))
        screen.addstr(*self.location, "V", curses.color_pair(PLAYER_COLOR))

class Villager(Unit):
    def __init__(self, location, health: int = None, capacity:int = None, 
                move_speed: int = 1) -> None:
        if capacity == None:
            self.capacity = VILLAGER_STATS["capacity"]
        if health == None:
            self.health = VILLAGER_STATS["health"]
        super().__init__(location, health)
        self.capacity = capacity 
        self.food: int = 0
        self.gold: int = 0
        self.wood: int = 0
        self.stone: int = 0
        self.time_on_task: int = 0
        self.gather_rate: int = 500
        self.move_speed = move_speed

    def gather(self, target, delta_time, gather_rate):
        """
        gather rate - units/time
        """
        self.time_on_task += delta_time
        delta_resource = delta_time*gather_rate
        full = False
        contents = self.food + self.wood + self.gold + self.stone + delta_resource
        if self.capacity <= contents:
            # if our villager is at full can't fit any more
            full = True

        if target.reource == Resources.FOOD:
            self.food += delta_resource if not full else (self.capacity - contents)
        elif target.resource == Resources.WOOD:
            self.wood += delta_resource if not full else (self.capacity - contents)
        elif target.resource == Resources.GOLD:
            self.gold += delta_resource if not full else (self.capacity - contents)
        elif target.resource == Resources.STONE:
            self.stone += delta_resource if not full else (self.capacity - contents)

    def step(self, location):
        self.prev_location = self.location
        direction = (location[0] - self.location[0], 
                     location[1] - self.location[1])
        direction = (direction[0]//abs(direction[0]) if direction[0] != 0 else 0,
                     direction[1]//abs(direction[1]) if direction[1] != 0 else 0)
        self.location = (self.location[0] + direction[0],
                         self.location[1] + direction[1])

    def move_to_location(self, location, delta_time) -> bool:
        """
        returns whether location has been reached
        """
        delta_time
        return self.location == location

class Soldier(Unit):
    def __init__(self, location, health: int, level: int) -> None:
        super().__init__(location, health)
        self.level = level
        self.hit_rate: int = 500

    def battle(self, target: Unit, difficulty: float, delta_time):
        """
        difficulty should be a float from 0 to 1 with the larger the number the 
        less likely the target is to die on any particular hit
        return True they died
        """
        def hit(difficulty):
            if random() > difficulty:
                return True
            else:
                return False



        


