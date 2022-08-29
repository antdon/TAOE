from typing import List 
import itertools
from constants import *
from incidental import Berry, Rocks, Tree, Vein

class Map:
    pass

class Tile:
    def __init__(self, coordinate: tuple[int, int], tilemap: Map) -> None:
        self.coordinate = coordinate
        self.tilemap = tilemap
        self.content = None
        self.users = set()

    def get_neighbours(self):
        squares = []
        for y,x in itertools.product(range(-1,2),repeat=2):
            if y == x == 0:
                pass
            else:
                n = self.tilemap.grid.get(
                    (self.coordinate[0]+y, self.coordinate[1]+x), None)
                if n:
                    squares.append(n)

        return squares

    def get_dist(self, coord: tuple[int, int]) -> int:
        return max(abs(self.coordinate[0] - coord[0]), abs(self.coordinate[1] - coord[1]))


class Map():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x), self) 
            for y,x in itertools.product(range(40), range(140))}

        #TODO: Make a bit more OO.
        for locations,resource in [(BERRY_LOCATIONS, Berry), 
                (TREE_LOCATIONS, Tree), (ROCK_LOCATIONS, Rocks), 
                (VEIN_LOCATIONS, Vein)]:
            for left,top,width,height in locations:
                for i,j in itertools.product(range(left,left+width), 
                                            range(top, top+height)):
                    self.grid[(i, j)].content = resource((i,j))












        

            








        

    


