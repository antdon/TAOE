from typing import List, Tuple
from unit import Soldier, Villager, Archer, Cavalry
from constants import *
from utils import InsufficientFundsException, InvalidCommandException, InvalidCoordinateException, InvalidResourceTypeException, WrongBuildingException

class Structure:
    buildable_units = []

    def __init__(self, location, player) -> None:
        self.location = location
        self.player = player
        self.player.structures.append(self)
        self.player.game.all_structures.append(self)
        self.grid = self.player.game.grid.grid
        self.rallypoint = None

    def create(self, alt_building, *args):
        if len(args) > 1:
            raise InvalidCommandException
        arg = args[0]
        for unit in self.buildable_units:
            if unit.enum_value == arg:
                if self.player.can_afford(unit.cost):
                    self.player.loses_resources(unit.cost)
                    new_unit = unit(self.location, self.player)
                    self.player.units.append(new_unit)
                    self.send_rally_command(new_unit)
                else:
                    raise InsufficientFundsException(read_cost(unit.name, 
                                                     unit.cost, "create"))
                break
        else:
            if arg in Units:
                # TODO: Instead of passing this as a parameter, just look 
                # at the unit to see where it can be built.
                raise WrongBuildingException(alt_building)

    def set_rallypoint(self, *args):
        pass
    
    def execute_command(self, command, *args):
        if command == "create":
            self.create(*args)
            return
        elif command == "rallypoint":
            self.set_rallypoint(*args)
            return
        raise InvalidCommandException

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
        return [self.grid.get(s, None) for s in squares if s]
        
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
        b = bytearray(b'S')
        b.append(int(self.enum_value.value) + 1)
        b.append(self.location[0]+1)
        b.append(self.location[1]+1)
        b.append(self.player.number + 1)
        b += b"..."
        return b
        # return {"type": self.enum_value, "location": self.location, 
        #         "color": self.player.color}




class Town_Hall(Structure):
    """
    A Town Hall is where a player should store their resources. 
    Other structures have only a singular resource they can store and only 
    a limited capacity of that resource. The Town Hall can store a bunch of 
    resources and can store infinite of all of them
    """
    enum_value = Buildings.TOWNHALL
    name = "townhall"
    buildable_units = [Villager]

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.size = (3, 6)
        # [food, wood, stone, gold]
        self.resources = [200, 300, 100, 100]

    def send_rally_command(self, unit):
        if self.rallypoint:
            unit.execute_command("gather", self.rallypoint)

    def set_rallypoint(self, *args):
        # raise Exception(args)
        if args and type(args[0]) == Resources:
            self.rallypoint = args[0]
        else:
            raise InvalidResourceTypeException

    def can_receive(self, resource):
        return True

    def create(self, *args):
        super().create("barracks", *args)

    @staticmethod
    def draw(screen, location, color) -> None:
        screen.addstr(location[0]+4, location[1] + 2, "      ", color)
        screen.addstr(location[0]+5, location[1] + 2, "  TH  ", color)
        screen.addstr(location[0]+6, location[1] + 2, "      ", color)

class House(Structure):
    enum_value = Buildings.HOUSE
    name = "house"

class Barracks(Structure):
    enum_value = Buildings.BARRACKS
    name = "barracks"
    buildable_units = [Soldier, Archer, Cavalry]

    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(BARRACKS_COST)
        super().__init__(location, player)

    def send_rally_command(self, unit):
        if self.rallypoint:
            unit.move(*self.rallypoint)
    
    def set_rallypoint(self, *args):
        if args and len(args) >= 2:
            t = (args[0], args[1])
            try:
                self.rallypoint = self.grid[t].coordinate
            except KeyError:
                raise InvalidCoordinateException

    @staticmethod
    def get_cost():
        return BARRACKS_COST

    def create(self, *args):
        super().create("townhall", *args)


    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, "Barr", color)
        screen.addstr(location[0]+5, location[1] + 2, "acks", color)


class Collector(Structure):
    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(COLLECTOR_COST)
        super().__init__(location, player)

    @staticmethod
    def get_cost():
        return COLLECTOR_COST


class Mine(Collector):
    enum_value = Buildings.MINE
    name = "mine"

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
    enum_value = Buildings.MILL
    name = "mill"

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
    enum_value = Buildings.LUMBERCAMP
    name = "lumbercamp"
    
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
    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site 
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building

class Quarry(Collector):
    enum_value = Buildings.LUMBERCAMP
    name = "quarry"

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.STONE

    def can_receive(self, resource):
        return resource in [Resources.STONE]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0]+4, location[1] + 2, " Qua", color)
        screen.addstr(location[0]+5, location[1] + 2, " rry", color)







