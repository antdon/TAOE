from typing import List, Tuple
from unit import Soldier, Villager
from constants import *

class Structure():
    def __init__(self, location, player) -> None:
        self.location = location
        self.player = player

    def get_neighbours(self):
        """ 
        Returns a list of squares that can deliver to this structure.
        """
        # TODO: Do with itertools and occupy places.
        squares = []
        for y in range(self.location[0]-1,self.location[0] + self.size[0]+2):
            squares.append((y, self.location[1]-1))
            squares.append((y, self.location[1]+self.size[1]))
        for x in range(self.location[1], self.location[1] + self.size[1]):
            squares.append((self.location[0]-1, x))
            squares.append((self.location[0]+self.size[0], x))
        # exit('hello')
        return [self.player.game.grid.grid[s] for s in squares]
        

    def update(self) -> None:
        pass

    def draw(self, screen) -> None:
        screen.addstr(*self.location, "      ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+1, self.location[1], "  TH  ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+2, self.location[1], "      ", curses.color_pair(PLAYER_COLOR))

class Town_Hall(Structure):
    """
    A Town Hall is where a player should store their resources. 
    Other structures have only a singular resource they can store and only 
    a limited capacity of that resource. The Town Hall can store a bunch of 
    resources and can store infinite of all of them
    """
    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.size = (3, 6)
        # [food, wood, stone, gold]
        self.resources = [0,0,0,0]

    def can_receive(self, resource):
        return True

    def create_villager(self):
        if self.resources[int(Resources.FOOD.value)] < 100:
            print("A villager costs 100 food to make")
        else:
            self.resources[int(Resources.FOOD.value)] -= 100
            self.player.units.append(Villager(self.location, self.player, 50))

    def create_soldier(self):
        if self.resources[int(Resources.FOOD.value)] < 100 or self.resources[int(Resources.GOLD.value)] < 100:
            print("A villager costs 100 food to make")
        else:
            self.resources[int(Resources.FOOD.value)] -= 100
            self.resources[int(Resources.GOLD.value)] -= 100
            self.player.units.append(Soldier(self.location,1))



class Mine(Structure):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location)
        self.rate_of_gain = rate_of_gain
        self.capacity = capacity

class Gold_Mine(Mine):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location, rate_of_gain, capacity)
        self.gold = 0
        self.resource = Resources.GOLD

    def mine(self):
        if self.gold < self.capacity:
            self.gold += self.rate_of_gain

class Stone_Mine(Mine):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location, rate_of_gain, capacity)
        self.stone = 0
        self.resource = Resources.STONE

    def mine(self):
        if self.stone < self.capacity:
            self.stone += self.rate_of_gain

class Build_Site(Structure):
    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site 
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building

            







