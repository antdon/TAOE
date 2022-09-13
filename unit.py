import time
from typing import List, Callable
from tilegrid import TileGrid
import random
from constants import *
from utils import *

class Unit:
    enum_value = -1
    icon = "?"

    def __init__(self, location, player) -> None:
        self.prev_location = location
        self.location = location
        self.player = player
        self.time_on_task: int = 0 
        self.attack_range = 1
        self.attack_speed = 300
        self.dead = False
        self.grid = self.player.game.grid
        self.player.game.all_units.append(self)

    def accrue_time(self, delta_time, goal) -> int:
        """
        Given the amount of time that has passed and the amount needed for the
        current goal, sets the new amount of time on task and returns the 
        number of times the goal is accrued.
        """
        self.time_on_task += delta_time
        steps = self.time_on_task // goal
        self.time_on_task %= goal
        return steps

    def die(self):
        self.player.units = [u for u in self.player.units if u != self]
        try:
            self.player.game.all_units.remove(self)
        except:
            pass
        self.dead = True
        self.player.game.screen.screen.addstr(self.location[0] + 4, 
                self.location[1] + 2, " ", curses.color_pair(BLANK_COLOR))
        self.player.game.screen.screen.refresh()
        try:
            self.container.remove(self)
        except:
            pass

    def set_desired_square(self, location):
        self.desired_square = location

    def step(self, location):
        self.prev_location = self.location
        direction = (location[0] - self.location[0], 
                     location[1] - self.location[1])
        direction = (direction[0]//abs(direction[0]) if direction[0] != 0 else 0,
                     direction[1]//abs(direction[1]) if direction[1] != 0 else 0)
        self.location = (self.location[0] + direction[0],
                         self.location[1] + direction[1])
        
    @staticmethod
    def draw(screen, prev_location, location, icon, color):
        screen.addstr(prev_location[0] + 4, prev_location[1] + 2, 
                        " ", curses.color_pair(BLANK_COLOR))
        screen.addstr(location[0] + 4, location[1] + 2, icon, color)
    
    def draw_info(self):
        return (type(self), self.prev_location, self.location, 
                self.icon, self.player.color)

    def set_state(self, action, target):
        self.state_action = action
        self.state_target = target

    def spend_time_until(self, num_steps: int, action: Callable, 
        until_state: Callable, rate: int):
        """
        Helper function for doing the given action until the unit reaches a
        desired state. When the unit does reach the desired state, the leftover
        accrued time is returned to time_on_task. 
        """
        for s in range(num_steps):
            action()
            if until_state():
                self.time_on_task += (num_steps - s - 1) * rate
                break

class Villager(Unit):
    enum_value = Units.VILLAGER
    name = "villager"
    cost = VILLAGER_COST
    icon = "V"

    def __init__(self, location, player, capacity:int = VILLAGER_CAPACITY, 
                move_speed: int = 500) -> None:
        super().__init__(location, player)
        self.capacity = capacity
        self.resources = {resource: 0 for resource in Resources}
        self.gather_rate: int = 300
        self.move_speed = move_speed
        self.deliver_square = None
        self.set_state(VillagerStates.IDLE, None)
        self.gathering_resource = None
        self.gather_square = None
        self.target_incidental = None
        self.container = self.player.villagers
        self.container.append(self)

    def build(self, TargetBuilding, *args):
        y,x = self.grid.validate_coordinate(*args)
        cost = TargetBuilding.get_cost()
        if self.player.can_afford(cost):
            self.set_desired_square((y,x))
            self.set_state(VillagerStates.BUILD, TargetBuilding)
            self.gather_square = None
        else:
            raise InsufficientFundsException(read_cost("building", cost, "build"))

    def execute_command(self, command, *args):
        if command not in ["gather", "build"]:
            raise InvalidCommandException
        if command == "gather":
            TargetResource = args[0]
            if type(TargetResource) != Resources:
                raise InvalidResourceTypeException
            self.set_state(VillagerStates.GATHER, TargetResource)
            self.update_target_square()
        elif command == "build":
            TargetBuilding = args[0]
            self.build(TargetBuilding, *args[1:])

    # TODO: Tidy this up, it's villager only, and only on gather.
    def update_target_square(self):
        if self.state_action == VillagerStates.GATHER:
            self.set_gather_square(*self.nearest_gatherable(self.state_target))
            self.set_deliver_square(self.nearest_deliverable(self.state_target))

    def set_gather_square(self, square, incidental, resource):
        if self.gather_square:
            self.grid[self.gather_square].users -= {self}
        self.gather_square = square
        self.target_incidental = incidental
        self.grid[square].users |= {self}
        self.player.debug = f"Villager is gathering {resource} at" \
            f" {self.grid[square]}"

    def set_deliver_square(self, square):
        self.deliver_square = square

    def capacity_reached(self):
        return sum(self.resources.values()) >= self.capacity

    def gather_step(self, target):
        self.resources[target.resource] = self.resources[target.resource] + 1

    def step(self, location):
        super().step(location)
        self.drop_if_possible()

    def gather(self, target, delta_time):
        """
        gather rate - units/time
        """
        gather_steps = self.accrue_time(delta_time, self.gather_rate)
        self.spend_time_until(
            gather_steps, lambda: self.gather_step(target), 
            self.capacity_reached, self.gather_rate
        )

    def drop_if_possible(self):
        # If next to a building that can take the carried resource, drop the resource.
        for structure in self.player.structures:
            if self.grid[self.location] in structure.get_neighbours():
                for resource in Resources:
                    if structure.can_receive(resource):
                        self.player.structures[0].resources[resource] += self.resources[resource]
                        self.resources[resource] = 0
                        self.update_target_square()

    def carried_resource(self):
        for resource in Resources:
            if self.resources[resource]: return resource
        return None

    def get_target_square(self):
        if self.state_action == VillagerStates.BUILD:
            return self.desired_square
        if self.state_action == VillagerStates.GATHER and self.needs_delivery(
            self.state_target):
            return self.nearest_deliverable(self.carried_resource())
        else:
            if not self.gather_square:
                self.update_target_square()
            return self.gather_square

    def update_move(self, delta_time):
        """
        Updates movement if possible.
        """
        if self.state_action == VillagerStates.IDLE:
            return
        if self.state_action == VillagerStates.BUILD:
            if self.location == self.desired_square:
                Building = self.state_target
                if self.player.can_afford(Building.get_cost()):
                    Building(self.location, self.player)
                    for villager in self.player.villagers:
                        villager.update_target_square()
                    self.set_state(*Building.get_next_state())
                else:
                    self.player.debug = "Not enough resources to build building."
                    self.set_state(VillagerStates.IDLE, None)
        if self.location == self.gather_square and not self.needs_delivery(
                                self.state_target):
            self.gather(self.target_incidental, delta_time)
        else:
            move_steps = self.accrue_time(delta_time, self.move_speed)
            target_location = self.get_target_square()
            self.spend_time_until(move_steps, 
                lambda: self.step(target_location),
                lambda: self.location == target_location, 
                self.move_speed)

    def needs_delivery(self, resource: Resources):
        return (any([self.resources[r] for r in Resources if 
            r != resource]) or self.capacity_reached())

    def nearest_gatherable(self, resource: Resources):
        """
        Returns a tuple: the square that is closest to the unit,
        and also the incidental that it will be gathering from.
        """
        game = self.player.game
        dist = (float('inf'), float('inf'))
        nearest = None
        target_incidental = None
        for incidental in game.incidentals:
            if resource == incidental.resource:
                for square in self.grid[incidental.location].get_neighbours():
                    curr_dist = (len(square.users), square.get_dist(self.location))
                    if curr_dist < dist:
                        nearest = square
                        dist = curr_dist
                        target_incidental = incidental
        return nearest.coordinate, target_incidental, target_incidental.resource

    def nearest_deliverable(self, resource: Resources):
        #TODO: A* Algorithm
        squares = []
        for structure in self.player.structures:
            if structure.can_receive(resource):
                squares += structure.get_neighbours()
        if not squares:
            exit(f"{self.player.structures}, {list(structure.location for structure in self.player.structures)} {squares}")
        return min(squares, key = lambda square: square.get_dist(self.gather_square)).coordinate
        
class Army(Unit):
    enum_value = -1
    def __init__(self, location, player):
        super().__init__(location, player)
        self.set_state(ArmyStates.IDLE, None)
        self.desired_square = None
        random.seed(self.player.next_random())
        self.random_state = random.getstate()

    def move(self, *args):
        # TODO: Make this set the desired square to a square rather than a coord
        y,x = self.grid.validate_coordinate(*args)
        self.set_state(ArmyStates.MOVE, None)
        self.set_desired_square((y,x))

    def execute_command(self, command, *args):
        if command not in ["attack", "move"]:
            raise InvalidCommandException
        if command == "attack":
            try:
                self.set_state(ArmyStates.ATTACK, args[0])
            except IndexError:
                raise InvalidCommandArgumentException
        if command == "move":
            self.move(*args)

    def nearest_attackable(self, target=None):
        squares = []
        # TODO: Enum problem.
        class_dict = {
            Units.ARCHER: Archer,
            Units.CAVALRY: Cavalry,
            Units.SOLDIER: Soldier,
            Units.VILLAGER: Villager
        }
        if target != None:
            for unit in self.player.enemy.units:
                if type(unit) == class_dict[target]:
                    squares += self.grid[unit.location].get_neighbours()
        else:
            for unit in self.player.enemy.units:
                squares += self.grid[unit.location].get_neighbours()
        return min(squares, key=lambda square: square.get_dist(self.location)).coordinate

    def is_attackable_unit(self, unit):
        return self.grid[unit.location].get_dist(self.location) <= self.attack_range

    def random_attack_result(self):
        random.setstate(self.random_state)
        retval = random.randrange(10)
        self.random_state = random.getstate()
        return retval

    def attack_once(self, target):
        r = self.random_attack_result()
        if r < 3:
            target.die()

    def attack_check(self):
        try:
            if self.state_action == ArmyStates.ATTACK:        
                nearest = self.nearest_attackable(self.state_target)
            else:
                nearest = self.nearest_attackable(None)
        except ValueError:
            self.set_state(ArmyStates.IDLE, None)
        attackables = list(filter(self.is_attackable_unit, self.player.enemy.units))
        if attackables:
        # TODO: Fix this stupid repeated call to the same object.
            actual_target = list(attackables)[0]
            attack_steps = self.accrue_time(0, self.attack_speed)
            self.spend_time_until(attack_steps, 
                lambda: self.attack_once(actual_target), 
                lambda: actual_target.dead,
                self.attack_speed)
            
    # TODO: Needs refactoring, unclear what behaviour is happening here.
    def update_move(self, delta_time):
        """
        Updates movement if possible.
        """
        if self.state_action == ArmyStates.ATTACK:
            try:
                self.desired_square = self.nearest_attackable(self.state_target)
            except ValueError:
                self.set_state(ArmyStates.IDLE, None)
        # Attack if possible.
        self.time_on_task += delta_time
        self.attack_check()
        if self.desired_square != None and self.location != self.desired_square:
            # Time not accrued here, because time accrued before checking attack
            move_steps = self.accrue_time(0, self.move_speed)
            target_location = self.desired_square
            self.spend_time_until(
                move_steps, lambda: self.step(target_location), 
                lambda: self.location == target_location, self.move_speed
            )
        if self.location == self.desired_square and self.state_action == ArmyStates.MOVE:
            self.set_state(ArmyStates.IDLE, None)

class Soldier(Army):
    enum_value = Units.SOLDIER
    name = "soldier"
    cost = SOLDIER_COST
    icon = "S"

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.move_speed = SOLDIER_SPEED
        self.container = self.player.soldiers
        self.container.append(self)

class Archer(Army):
    enum_value = Units.ARCHER
    name = "archer"
    cost = ARCHER_COST
    icon = "A"

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.attack_range = 5
        self.move_speed = ARCHER_SPEED
        self.container = self.player.archers
        self.container.append(self)

class Cavalry(Army):
    enum_value = Units.CAVALRY
    name = "cavalry"
    cost = CAVALRY_COST
    icon = "C"

    def __init__(self, location, player) -> None:
        super().__init__(location, player)
        self.move_speed = CAVALRY_SPEED
        self.container = self.player.cavalry
        self.container.append(self)