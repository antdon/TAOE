from typing import List, Tuple
from unit import Soldier, Villager, Archer, Cavalry
from constants import *

class Structure():
    def __init__(self, location, player) -> None:
        self.location = location
        self.player = player
        self.player.structures.append(self)

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
        return [self.player.game.grid.grid.get(s, None) for s in squares if s]
        

    def update(self) -> None:
        pass

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
        self.resources = [100,100,100,100]

    def can_receive(self, resource):
        return True

    def create_villager(self):
        # TODO: Build a function that compares cost dictionary.
        if self.resources[int(Resources.FOOD.value)] < VILLAGER_COST[Resources.FOOD]:
            self.player.debug = f"A villager costs {VILLAGER_COST[Resources.FOOD]} food to make"
        else:
            self.resources[int(Resources.FOOD.value)] -= VILLAGER_COST[Resources.FOOD]
            self.player.units.append(Villager(self.location, self.player))

    def create_soldier(self):
        if self.resources[int(Resources.FOOD.value)] < 60 or self.resources[int(Resources.GOLD.value)] < 40:
            self.player.debug = "A soldier costs 60 food and 40 wood to make"
        else:
            self.resources[int(Resources.FOOD.value)] -= 60
            self.resources[int(Resources.GOLD.value)] -= 40
            self.player.units.append(Soldier(self.location,self.player))

    
    def create_archer(self):
        if self.resources[int(Resources.FOOD.value)] < 40 or self.resources[int(Resources.WOOD.value)] < 25:
            self.player.debug = "An archer costs 40 food and 25 wood to make"
        else:
            self.resources[int(Resources.FOOD.value)] -= 40
            self.resources[int(Resources.WOOD.value)] -= 25
            self.player.units.append(Archer(self.location,self.player))
    
    def create_cavalry(self):
        if self.resources[int(Resources.FOOD.value)] < 100 or self.resources[int(Resources.GOLD.value)] < 60:
            self.player.debug = "A cavalry costs 100 food and 60 gold to make"
        else:
            self.resources[int(Resources.FOOD.value)] -= 100
            self.resources[int(Resources.GOLD.value)] -= 60
            self.player.units.append(Cavalry(self.location,self.player))

    def draw(self, screen) -> None:
        screen.addstr(self.location[0]+4, self.location[1] + 2, "      ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+5, self.location[1] + 2, "  TH  ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+6, self.location[1] + 2, "      ", curses.color_pair(PLAYER_COLOR))

class House(Structure):
    pass

class Collector(Structure):
    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(COLLECTOR_COST)
        super().__init__(location, player)

    @staticmethod
    def get_cost():
        return COLLECTOR_COST


class Mine(Collector):

    def can_receive(self, resource):
        return resource in [Resources.GOLD, Resources.STONE]

    def draw(self, screen):
        screen.addstr(self.location[0]+4, self.location[1] + 2, " MI ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+5, self.location[1] + 2, " NE ", curses.color_pair(PLAYER_COLOR))


class Mill(Collector):
    def can_receive(self, resource):
        return resource in [Resources.FOOD]

    def draw(self, screen):
        screen.addstr(self.location[0]+4, self.location[1] + 2, " MI ", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+5, self.location[1] + 2, " LL ", curses.color_pair(PLAYER_COLOR))

class LumberCamp(Collector):
    def can_receive(self, resource):
        return resource in [Resources.WOOD]

    def draw(self, screen):
        screen.addstr(self.location[0]+4, self.location[1] + 2, " Lum", curses.color_pair(PLAYER_COLOR))
        screen.addstr(self.location[0]+5, self.location[1] + 2, "Camp", curses.color_pair(PLAYER_COLOR))
        

class Build_Site(Structure):
    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site 
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building

            







