import time
from typing import List
from tilegrid import TileGrid
import random
from constants import *
from utils import *

class Unit:
    enum_value = -1

    def __init__(self, location, player, icon) -> None:
        self.prev_location = location
        self.location = location
        self.player = player
        self.icon = icon
        self.time_on_task: int = 0 
        self.attack_range = 1
        self.attack_speed = 300
        self.dead = False
        self.grid = self.player.game.grid.grid
        self.player.game.all_units.append(self)

    def die(self):
        self.player.units = [u for u in self.player.units if u != self]
        self.player.game.all_units = [u for u in self.player.game.all_units if u != self]
        self.dead = True
        self.player.game.screen.screen.addstr(self.location[0] + 4, self.location[1] + 2, 
                        " ", curses.color_pair(BLANK_COLOR))
        self.player.game.screen.screen.refresh()

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

    def neighbourhood(self, map: TileGrid):
        surroundings = []
        for tile in map:
            if tile.content:
                surroundings.append((tile.content, tile.coordinate)) 
        return surroundings
        
    @staticmethod
    def draw(screen, prev_location, location, icon, color):
        screen.addstr(prev_location[0] + 4, prev_location[1] + 2, 
                        " ", curses.color_pair(BLANK_COLOR))
        screen.addstr(location[0] + 4, location[1] + 2, icon, color)
    
    def draw_info(self):
        b = bytearray(b"U")
        b.append(int(self.enum_value.value) + 1)
        b.append(self.prev_location[0]+1)
        b.append(self.prev_location[1]+1)
        b.append(self.location[0]+1)
        b.append(self.location[1]+1)
        b += self.icon.encode()
        b.append(self.player.number + 1)
        return b
        # return {"type": self.enum_value, "prev_location": self.prev_location, 
        #     "location": self.location, "icon": self.icon, 
        #     "color": self.player.color}

class Villager(Unit):
    enum_value = Units.VILLAGER
    name = "villager"
    cost = VILLAGER_COST

    def __init__(self, location, player, capacity:int = VILLAGER_CAPACITY, 
                move_speed: int = 500) -> None:
        super().__init__(location, player, "V")
        self.capacity = capacity
        self.resources = [0,0,0,0]
        self.gather_rate: int = 300
        self.move_speed = move_speed
        self.deliver_square = None
        self.state_action = VillagerStates.IDLE
        self.state_target = None
        self.gathering_resource = None
        self.gather_square = None
        self.target_incidental = None
        self.debug_info = ""
        self.player.villagers.append(self)

    def build(self, TargetBuilding, *args):
        t=  (args[0], args[1])
        try:
            y,x = self.grid[t].coordinate
        except KeyError:
            raise InvalidCoordinateException
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
            self.set_state(VillagerStates.GATHER, TargetResource)
            self.update_target_square()
        if command == "build":
            TargetBuilding = args[0]
            self.build(TargetBuilding, *args[1:])

    def stop(self):
        self.state_action = VillagerStates.IDLE
        self.state_target = None

    def set_gather_square(self, square, incidental, resource):
        if self.gather_square:
            self.grid[self.gather_square].users -= {self}
        self.gather_square = square
        self.target_incidental = incidental
        self.grid[square].users |= {self}
        self.player.debug = f"{square} {incidental} {resource}"

    def set_deliver_square(self, square):
        self.deliver_square = square

    def capacity_reached(self):
        return sum(self.resources) >= self.capacity

    def gather_step(self, target):
        self.resources[int(target.resource.value)] = self.resources[int(target.resource.value)] + 1

    def step(self, location):
        super().step(location)
        self.drop_if_possible()

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
        # If next to a building that can take the carried resource, drop the resource.
        for structure in self.player.structures:
            if self.grid[self.location] in structure.get_neighbours():
                for i,x in enumerate(self.resources):
                    if structure.can_receive(Resources(i)):
                        self.player.structures[0].resources[i] += x
                        self.resources[i] = 0
                        self.update_target_square()

    def carried_resource(self):
        for i,x in enumerate(self.resources):
            if x: return Resources(i)
        return None

    def get_target_square(self):
        self.debug += str(self.state_target)
        if self.state_action == VillagerStates.BUILD:
            return self.desired_square
        self.debug += str(self.state_target)
        # self.debug = "a"
        if self.state_action == VillagerStates.GATHER and self.needs_delivery(
            self.state_target):
            return self.nearest_deliverable(self.carried_resource())
        else:
            return self.gather_square

    def get_debug_info(self):
        return (f"{self.debug_info}")

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
        # self.debug = "b"
        if self.location == self.gather_square and not self.needs_delivery(
                                self.state_target):
            
            self.gather(self.target_incidental, delta_time)
        else:
            self.time_on_task += delta_time
            move_steps = self.time_on_task // self.move_speed
            self.time_on_task %= self.move_speed
            self.debug = str(self.state_target)
            target_location = self.get_target_square()
            for s in range(move_steps):
                self.step(target_location)
                if self.location == target_location:
                    self.time_on_task += (move_steps - s - 1) * self.move_speed
                    break
            

    def set_state(self, action, target):
        self.state_action = action
        self.state_target = target
        self.update_target_square()

    def needs_delivery(self, resource: Resources):
        if resource == None:
            exit(f"{self.debug}")
        return (any([x for i,x in enumerate(self.resources) if 
            i != int(resource.value)]) or self.capacity_reached())
        

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
                for square in game.grid.grid[incidental.location].get_neighbours():
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

    def update_target_square(self):
        if self.state_action == VillagerStates.GATHER:
            if type(self.state_target) == Resources:
                self.set_gather_square(*self.nearest_gatherable(self.state_target))
                self.set_deliver_square(self.nearest_deliverable(self.state_target))
                
        if self.gather_square == None:
            pass
        if self.deliver_square == None:
            pass
    
    def die(self):
        super().die()
        self.player.villagers = [u for u in self.player.villagers if u != self]
        
class Army(Unit):
    enum_value = -1
    def __init__(self, location, player, icon):
        super().__init__(location, player, icon)
        self.state_action = ArmyStates.IDLE
        self.state_target = None

        random.seed(self.player.next_random())
        self.random_state = random.getstate()

    def stop(self):
        self.state_action = ArmyStates.IDLE
        self.state_target = None

    def move(self, *args):
        # TODO: Make this set the desired square to a square rather than a coord
        try:
            y,x = self.grid[(args[0], args[1])].coordinate
        except KeyError:
            raise InvalidCoordinateException
        self.state_action = ArmyStates.MOVE
        self.state_target = None
        self.set_desired_square((y,x))

    def execute_command(self, command, *args):
        if command not in ["attack", "move"]:
            raise InvalidCommandException
        if command == "attack":
            self.set_attacking(args[0])
        if command == "move":
            self.move(*args)

    def nearest_attackable(self, target=None):
        squares = []
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
            self.player.debug = "Dead"

    def attack_check(self):
        try:
            if self.state_action == ArmyStates.ATTACK:        
                nearest = self.nearest_attackable(self.state_target)
            else:
                nearest = self.nearest_attackable(None)
        except ValueError:
            self.state_action = ArmyStates.IDLE
            self.state_target = None
        attackables = list(filter(self.is_attackable_unit, self.player.enemy.units))
        if attackables:
        # TODO: Fix this stupid repeated call to the same object.
            actual_target = list(attackables)[0]
            attack_steps = self.time_on_task // self.attack_speed
            self.time_on_task %= self.attack_speed
            for a in range(attack_steps):
                self.attack_once(actual_target)
                if actual_target.dead:
                    pass            
            
    def update_move(self, delta_time):
        """
        Updates movement if possible.
        """
        if self.state_action == ArmyStates.ATTACK:
            try:
                self.desired_square = self.nearest_attackable(self.state_target)
            except ValueError:
                self.state_action = ArmyStates.IDLE
                self.state_target = None
        if self.desired_square != None and self.location != self.desired_square:
            self.time_on_task += delta_time
            s = f"{self.time_on_task}"
            self.attack_check()
            s += f"{self.time_on_task}"
            move_steps = self.time_on_task // self.move_speed
            self.time_on_task %= self.move_speed
            target_location = self.desired_square
            for s in range(move_steps):
                self.step(target_location)
                if self.location == target_location:
                    self.time_on_task += (move_steps - s - 1) * self.move_speed
                    self.state_action = ArmyStates.IDLE
                    break
        else:
            self.time_on_task += delta_time
            self.attack_check()
    
    def set_attacking(self, target_unit):
        self.state_action = ArmyStates.ATTACK
        self.state_target = target_unit

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

        self.time_on_task += delta_time
        move_steps = self.time_on_task // self.hit_rate
        self.time_on_task %= self.hit_rate
        for s in range(move_steps):
            killed = hit(difficulty)
            if killed:
                self.time_on_task += (move_steps - s - 1) * self.hit_rate
                break
        return killed

class Soldier(Army):
    enum_value = Units.SOLDIER
    name = "soldier"
    cost = SOLDIER_COST

    def __init__(self, location, player, level: int = 1) -> None:
        super().__init__(location, player, "S")
        self.level = level
        self.hit_rate: int = 500
        self.desired_square = None
        self.move_speed = SOLDIER_SPEED
        self.player.soldiers.append(self)

    def get_index(self):
        if self in self.player.soldiers:
            return self.player.soldiers.index(self)
        else:
            return None

    def die(self):
        super().die()
        self.player.soldiers = [u for u in self.player.soldiers if u != self]

class Archer(Army):
    enum_value = Units.ARCHER
    name = "archer"
    cost = ARCHER_COST

    def __init__(self, location, player, level: int = 1) -> None:
        super().__init__(location, player, "A")
        self.level = level
        self.hit_rate: int = 500
        self.attack_range = 5
        self.desired_square = None
        self.move_speed = ARCHER_SPEED
        self.player.archers.append(self)

    def get_index(self):
        if self in self.player.archers:
            return self.player.archers.index(self)
        else:
            return None
    
    def die(self):
        super().die()
        self.player.archers = [u for u in self.player.archers if u != self]

class Cavalry(Army):
    enum_value = Units.CAVALRY
    name = "cavalry"
    cost = CAVALRY_COST

    def __init__(self, location, player, level: int =1) -> None:
        super().__init__(location, player, "C")
        self.level = level
        self.hit_rate: int = 500
        self.desired_square = None
        self.move_speed = CAVALRY_SPEED
        self.player.cavalry.append(self)

    def get_index(self):
        if self in self.player.cavalry:
            return self.player.cavalry.index(self)
        else:
            return None
    
    def die(self):
        super().die()
        self.player.cavalry = [u for u in self.player.cavalry if u != self]