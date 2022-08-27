from importlib.resources import Resource
import time
from incidental import Animal, Tree
from random import random
from constants import *



class Unit():
    def __init__(self, location, health: int, player) -> None:
        self.prev_location = location
        self.location = location
        self.health = health
        self.player = player

    def draw(self, screen):
        screen.addstr(*self.prev_location, " ", curses.color_pair(BLANK_COLOR))
        screen.addstr(*self.location, "V", curses.color_pair(PLAYER_COLOR))

class Villager(Unit):
    def __init__(self, location, player, health: int = None, capacity:int = None, 
                move_speed: int = 500) -> None:
        if capacity == None:
            capacity = VILLAGER_STATS["capacity"]
        if health == None:
            health = VILLAGER_STATS["health"]
        super().__init__(location, health, player)
        self.capacity = capacity 
        self.resources = [0,0,0,0]
        self.time_on_task: int = 0
        self.gather_rate: int = 300
        self.move_speed = move_speed

    def capacity_reached(self):
        return sum(self.resources) >= self.capacity

    def gather_step(self, target):
        self.resources[int(target.resource.value)] = self.resources[int(target.resource.value)] + 1

    def gather(self, target, delta_time):
        """
        gather rate - units/time
        """
        self.time_on_task += delta_time
        gather_steps = self.time_on_task // self.gather_rate
        self.time_on_task %= self.gather_rate

        for s in range(gather_steps):
            self.gather_step(target)
            if self.capacity_reached():
                self.time_on_task += (gather_steps - s - 1) * self.gather_rate
                break

    def drop_if_possible(self):
        # If next to Town Hall, drop resources
        if self.location == (21, 16):
            for i,x in enumerate(self.resources):
                self.player.structures[0].resources[i] += x
                self.resources[i] = 0

    def step(self, location):
        self.prev_location = self.location
        direction = (location[0] - self.location[0], 
                     location[1] - self.location[1])
        direction = (direction[0]//abs(direction[0]) if direction[0] != 0 else 0,
                     direction[1]//abs(direction[1]) if direction[1] != 0 else 0)
        self.location = (self.location[0] + direction[0],
                         self.location[1] + direction[1])
        self.drop_if_possible()

    def move_to_location(self, location, delta_time) -> bool:
        """
        returns whether location has been reached
        """
        self.time_on_task += delta_time
        move_steps = self.time_on_task // self.move_speed
        self.time_on_task %= self.move_speed
        for s in range(move_steps):
            self.step(location)
            if self.location == location:
                self.time_on_task += (move_steps - s - 1) * self.move_speed
                break
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



        


