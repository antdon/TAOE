from importlib.resources import Resource
import time
from typing import List
from map import Map
from incidental import Animal, Tree
from random import random
from constants import *



class Unit():
    def __init__(self, location, player) -> None:
        self.prev_location = location
        self.location = location
        self.player = player

    def neighbourhood(self, map: Map):
        surroundings = []
        for tile in map:
            if tile.content:
                surroundings.append((tile.content, tile.coordinate)) 
        return surroundings
        

    def draw(self, screen):
        screen.addstr(*self.prev_location, " ", curses.color_pair(BLANK_COLOR))
        screen.addstr(*self.location, "V", curses.color_pair(PLAYER_COLOR))

class Villager(Unit):
    def __init__(self, location, player, capacity:int = None, 
                move_speed: int = 500) -> None:
        if capacity == None:
            capacity = VILLAGER_STATS["capacity"]
        super().__init__(location, player)
        self.capacity = capacity 
        self.resources = [0,0,0,0]
        self.time_on_task: int = 0
        self.gather_rate: int = 300
        self.move_speed = move_speed
        #TODO: Stop the default being wood
        self.set_deliver_square((21, 16))
        self.gathering_resource = None
        self.desired_resource = None
        self.target_incidental = None
        # self.set_gather_square((11, 26), Resources.WOOD)


    def set_gather_square(self, square, incidental, resource):
        self.gather_square = square
        self.target_incidental = incidental
        self.desired_resource = resource
        self.player.debug = f"{square} {incidental} {resource}"

    def set_deliver_square(self, square):
        self.deliver_square = square

    def capacity_reached(self):
        return sum(self.resources) >= self.capacity

    def gather_step(self, target):
        self.resources[int(target.resources[0].value)] = self.resources[int(target.resources[0].value)] + 1

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

    def get_target_square(self):
        if self.capacity_reached():
            return self.deliver_square
        else:
            return self.gather_square

    def update_move(self, delta_time):
        """
        Updates movement if possible.
        """
        # TODO: Make this general case, not just wood.
        if self.location == self.gather_square and not self.needs_delivery(
                                self.desired_resource):
            self.gather(self.target_incidental, delta_time)
        else:
            self.time_on_task += delta_time
            move_steps = self.time_on_task // self.move_speed
            self.time_on_task %= self.move_speed
            target_location = self.get_target_square()
            for s in range(move_steps):
                self.step(target_location)
                if self.location == target_location:
                    self.time_on_task += (move_steps - s - 1) * self.move_speed
                    break
            

    def set_state(self, action, target):
        self.state_action = action
        self.state_target = target

    def needs_delivery(self, resource: Resources):
        if resource == None:
            exit(f"{resource}")
        return (any([x for i,x in enumerate(self.resources) if i != int(resource.value)]) 
            or self.capacity_reached())

    def nearest_gatherable(self, resource: Resources):
        squares = []
        game = self.player.game
        for incidental in game.incidentals:
            if resource in incidental.resources:
                squares += game.map.grid[incidental.location].get_neighbours()
        return min(squares, key = lambda square: square.get_dist(self.location)).coordinate

    def nearest_deliverable(self, resource: Resources):
        squares = []
        for structure in self.player.structures:
            if structure.can_receive(resource):
                squares += structure.get_neighbours()
        return min(squares, key = lambda square: square.get_dist(self.location)).coordinate

    def nearest_gatherable(self, resource: Resources, grid : Map):
        squares = []
        for tile in grid.grid.values():
            if tile.content and resource in tile.content.resources:
                squares.append(tile)
        return min(squares, key = lambda square: abs(square.coordinate[0] - self.location[0]) + abs(square.coordinate[1] - self.location[1]))

    def update_target_square(self, grid):
        if self.state_action == VillagerStates.GATHER:
            if self.state_target == FoodTypes.BERRIES:
                # If anything we're carrying isn't food...
                self.set_gather_square(self.nearest_gatherable(FoodTypes.BERRIES))
                if self.needs_delivery(Resources.FOOD):
                    # Find a place to deliver it...
                    self.set_deliver_square(self.nearest_deliverable(FoodTypes.BERRIES))
                    
                # Find a berry square.
                
                pass
        if self.gather_square == None:
            pass
        if self.deliver_square == None:
            pass
        

class Soldier(Unit):
    def __init__(self, location, level: int) -> None:
        super().__init__(location)
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

        self.time_on_task += delta_time
        move_steps = self.time_on_task // self.hit_rate
        self.time_on_task %= self.hit_rate
        for s in range(move_steps):
            killed = hit(difficulty)
            if killed:
                self.time_on_task += (move_steps - s - 1) * self.hit_rate
                break
        return killed


        


