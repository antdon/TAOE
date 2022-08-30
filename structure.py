from typing import List, Tuple
from unit import Soldier, Villager, Archer, Cavalry
from constants import *

class Structure:
    name = "Structure"

    def __init__(self, location, player) -> None:
        self.location = location
        self.player = player
        self.player.structures.append(self)
        self.player.game.all_structures.append(self)

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
        
    @staticmethod
    def get_next_state():
        return VillagerStates.IDLE, None

    def can_receive(self, resource):
        return resource in []

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, "Buil", color)
        screen.addstr(location[0]+5, location[1] + 2, "ding", color)

    def draw_info(self):
        return {"type": self.name, "location": self.location, 
                "color": self.player.color}


class Town_Hall(Structure):
    """
    A Town Hall is where a player should store their resources. 
    Other structures have only a singular resource they can store and only 
    a limited capacity of that resource. The Town Hall can store a bunch of 
    resources and can store infinite of all of them
    """
    name = "Town_Hall"

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.size = (3, 6)
        # [food, wood, stone, gold]
        self.resources = [200, 300, 100, 100]

    def can_receive(self, resource):
        return True

    def create_villager(self):
        # TODO: Build a function that compares cost dictionary.
        if self.resources[int(Resources.FOOD.value)] < VILLAGER_COST[Resources.FOOD]:
            self.player.debug = f"A villager costs {VILLAGER_COST[Resources.FOOD]} food to make"
        else:
            self.resources[int(Resources.FOOD.value)] -= VILLAGER_COST[Resources.FOOD]
            self.player.units.append(Villager(self.location, self.player))

    @staticmethod
    def draw(screen, location, color) -> None:
        screen.addstr(location[0]+4, location[1] + 2, "      ", color)
        screen.addstr(location[0]+5, location[1] + 2, "  TH  ", color)
        screen.addstr(location[0]+6, location[1] + 2, "      ", color)

    

class House(Structure):
    name = "House"

class Barracks(Structure):
    name = "Barracks"

    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(BARRACKS_COST)
        super().__init__(location, player)

    @staticmethod
    def get_cost():
        return BARRACKS_COST

    def create_soldier(self):
        if self.player.can_afford(SOLDIER_COST):
            self.player.loses_resources(SOLDIER_COST)
            self.player.units.append(Soldier(self.location,self.player))
        else:
            self.player.debug = read_cost("Soldier", SOLDIER_COST)
    
    def create_archer(self):
        if self.player.can_afford(ARCHER_COST):
            self.player.loses_resources(ARCHER_COST)
            self.player.units.append(Archer(self.location,self.player))
        else:
            self.player.debug = read_cost("Archer", ARCHER_COST)
    
    def create_cavalry(self):
        if self.player.can_afford(CAVALRY_COST):
            self.player.loses_resources(CAVALRY_COST)
            self.player.units.append(Cavalry(self.location,self.player))
        else:
            self.player.debug = read_cost("Cavalry", CAVALRY_COST)

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, "Barr", color)
        screen.addstr(location[0]+5, location[1] + 2, "acks", color)


class Collector(Structure):
    name = "Collector"
    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(COLLECTOR_COST)
        super().__init__(location, player)

    @staticmethod
    def get_cost():
        return COLLECTOR_COST


class Mine(Collector):
    name = "Mine"

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.GOLD

    def can_receive(self, resource):
        return resource in [Resources.GOLD, Resources.STONE]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, " MI ", color)
        screen.addstr(location[0]+5, location[1] + 2, " NE ", color)


class Mill(Collector):
    name = "Mill"

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.FOOD

    def can_receive(self, resource):
        return resource in [Resources.FOOD]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, " MI ", color)
        screen.addstr(location[0]+5, location[1] + 2, " LL ", color)

class LumberCamp(Collector):
    name = "LumberCamp"
    
    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.WOOD

    def can_receive(self, resource):
        return resource in [Resources.WOOD]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, " Lum", color)
        screen.addstr(location[0]+5, location[1] + 2, "Camp", color)
        

class Build_Site(Structure):
    name = "Build_Site"
    
    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site 
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building

            







