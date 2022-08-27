from importlib.resources import Resource
from incidental import Animal, Tree
from random import choice
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
                move_speed: int = 500) -> None:
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

    def capacity_reached(self):
        return sum([self.food, self.wood, self.gold, self.stone])

    def gather_step(self, target):
        target.resource_name

    def gather(self, target, delta_time):
        """
        gather rate - units/time
        """
        self.time_on_task += delta_time
        gather_steps = self.time_on_task // self.gather_rate
        self.time_on_task %= self.gather_rate

        for s in gather_steps:
            self.gather_step(target)
            if self.capacity_reached():
                self.time_on_task += (gather_steps - s - 1) * self.gather_rate
                break

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

