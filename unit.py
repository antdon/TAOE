from asyncio import gather
from incidental import Animal, Tree
from structure import Gold_Mine, Stone_Mine
from random import choice



class Unit():
    def __init__(self, location, health: int) -> None:
        self.location = location
        self.health = health

    def draw(self, stdscr):
        
        pass

class Villager(Unit):
    def __init__(self, location, health: int, capacity:int, move_speed = 1) -> None:
        super().__init__(location, health)
        self.capacity = capacity 
        self.food: int = 0
        self.gold: int = 0
        self.wood: int = 0
        self.stone: int = 0
        self.time_on_task: int = 0
        self.gather_rate: int = 500
        self.move_speed = move_speed

    def gather(self, target, delta_time, gather_rate):
        """
        gather rate - units/time
        """
        self.time_on_task += delta_time
        delta_resource = delta_time*gather_rate
        full = False
        contents = self.food + self.wood + self.gold + self.stone + delta_resource
        if self.capacity <= contents:
            # if our villager is at full can't fit any more
            full = True

        if type(target) == Animal:
            self.food += delta_resource if not full else (self.capacity - contents)
        elif type(target) == Tree:
            self.wood += delta_resource if not full else (self.capacity - contents)
        elif type(target) == Gold_Mine:
            self.gold += delta_resource if not full else (self.capacity - contents)
        elif type(target) == Stone_Mine:
            self.stone += delta_resource if not full else (self.capacity - contents)

    def move_to_location(self, location, delta_time) -> bool:
        """
        returns whether location has been reached
        """
        direction = None
        delta_location = delta_time * self.move_speed
        if self.location[0] != location[0] and self.location[1] != location[1]:
            direction = choice("vertical", "horizontal")
        elif self.location[0] != location[0]:
            direction = "horizontal"
        elif self.location[1] != location[1]:
            direction = "vertical"
        else:
            return True

        if direction == "horizontal":
            if self.location[0] > location[0]:
                self.location[0] += delta_location
            else:
                self.location[0] -= delta_location
        else:
            if self.location[1] > location[1]:
                self.location[1] += delta_location
            else:
                self.location[1] -= delta_location

        if self.location == location:
            return True
        else:
            return False
            
            



        


        

class Soldier(Unit):
    def __init__(self, location, health: int, level: int) -> None:
        super().__init__(location, health)
        self.level = level

