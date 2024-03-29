from typing import List, Tuple
from unit import Soldier, Villager, Archer, Cavalry
from constants import *
from utils import *


class Structure:
    buildable_units = []
    name = "structure"

    def __init__(self, location, player) -> None:
        self.location = location
        self.player = player
        self.name = "structure"
        self.player.game.all_structures.append(self)
        self.grid = self.player.game.grid
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
                    raise InsufficientFundsException(
                        read_cost(unit.name, unit.cost, "create")
                    )
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
            if len(args) == 0:
                raise InvalidUnitTypeException
            self.create(*args)
            return
        elif command == "rallypoint":
            if len(args) == 0:
                raise InvalidCoordinateException
            self.set_rallypoint(*args)
            return
        raise InvalidCommandException

    def get_neighbours(self):
        """
        Returns a list of squares that can deliver to this structure.
        """
        squares = []
        for y in range(self.location[0] - 1, self.location[0] + self.size[0] + 2):
            squares.append((y, self.location[1] - 1))
            squares.append((y, self.location[1] + self.size[1]))
        for x in range(self.location[1], self.location[1] + self.size[1]):
            squares.append((self.location[0] - 1, x))
            squares.append((self.location[0] + self.size[0], x))
        return [self.grid.grid.get(s, None) for s in squares if s]

    @staticmethod
    def get_next_state():
        return VillagerStates.IDLE, None

    def can_receive(self, resource):
        return resource in []

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, "Buil", color)
        screen.addstr(location[0] + 5, location[1] + 2, "ding", color)

    def draw_info(self):
        return (type(self), self.location, self.player.color)


class TownHall(Structure):
    """
    A Town Hall is where a player should store their resources.
    Other structures have only a singular resource they can store and only
    a limited capacity of that resource. The Town Hall can store a bunch of
    resources and can store infinite of all of them
    """

    enum_value = Structures.TOWNHALL
    buildable_units = [Villager]
    name = "townhall"

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.size = (3, 6)
        self.name = "townhall"
        # [food, wood, stone, gold]
        self.resources = dict(zip(Resources, [200, 300, 100, 100]))

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
        screen.addstr(location[0] + 4, location[1] + 2, "      ", color)
        screen.addstr(location[0] + 5, location[1] + 2, "  TH  ", color)
        screen.addstr(location[0] + 6, location[1] + 2, "      ", color)


class House(Structure):
    enum_value = Structures.HOUSE

    def __init__(self, location, player) -> None:
        self.name = "house"
        super().__init__(location, player)


class Barracks(Structure):
    enum_value = Structures.BARRACKS
    name = "barracks"
    buildable_units = [Soldier, Archer, Cavalry]

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.size = (2, 4)
        self.name = "barracks"
        player.loses_resources(BARRACKS_COST)

    def send_rally_command(self, unit):
        if self.rallypoint:
            unit.move(*self.rallypoint)

    def set_rallypoint(self, *args):
        if args and len(args) >= 2:
            t = self.grid.validate_coordinate(*args)
            self.rallypoint = t

    @staticmethod
    def get_cost():
        return BARRACKS_COST

    def create(self, *args):
        super().create("townhall", *args)

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, "Barr", color)
        screen.addstr(location[0] + 5, location[1] + 2, "acks", color)


class Collector(Structure):
    def __init__(self, location, player) -> None:
        self.size = (2, 4)
        player.loses_resources(COLLECTOR_COST)
        super().__init__(location, player)

    @staticmethod
    def get_cost():
        return COLLECTOR_COST


class Mine(Collector):
    enum_value = Structures.MINE
    name = "mine"

    def __init__(self, location, player) -> None:
        self.name = "mine"
        super().__init__(location, player)

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.GOLD

    def can_receive(self, resource):
        return resource in [Resources.GOLD, Resources.STONE]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, " MI ", color)
        screen.addstr(location[0] + 5, location[1] + 2, " NE ", color)


class Mill(Collector):
    enum_value = Structures.MILL
    name = "mill"

    def __init__(self, location, player) -> None:
        self.name = "mill"
        super().__init__(location, player)

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.FOOD

    def can_receive(self, resource):
        return resource in [Resources.FOOD]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, " MI ", color)
        screen.addstr(location[0] + 5, location[1] + 2, " LL ", color)


class LumberCamp(Collector):
    enum_value = Structures.LUMBERCAMP
    name = "lumbercamp"

    def __init__(self, location, player) -> None:
        self.name = "lumbercamp"
        super().__init__(location, player)

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.WOOD

    def can_receive(self, resource):
        return resource in [Resources.WOOD]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, " Lum", color)
        screen.addstr(location[0] + 5, location[1] + 2, "Camp", color)


class Build_Site(Structure):
    name = "buildsite"

    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building
        self.name = "buildsite"


class Quarry(Collector):
    enum_value = Structures.QUARRY
    name = "quarry"

    def __init__(self, location, player) -> None:
        self.name = "quarry"
        super().__init__(location, player)

    @staticmethod
    def get_next_state():
        return VillagerStates.GATHER, Resources.STONE

    def can_receive(self, resource):
        return resource in [Resources.STONE]

    @staticmethod
    def draw(screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, " Qua", color)
        screen.addstr(location[0] + 5, location[1] + 2, " rry", color)
