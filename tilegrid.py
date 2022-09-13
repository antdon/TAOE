from typing import List, Tuple
import itertools
from constants import *
from incidental import Berry, Rocks, Tree, Vein
from utils import InvalidCoordinateException

class TileGrid:
    pass

class Tile:
    def __init__(self, coordinate: Tuple[int, int], tilemap: TileGrid) -> None:
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

    def get_dist(self, coord: Tuple[int, int]) -> int:
        return max( abs(self.coordinate[0] - coord[0]), 
                    abs(self.coordinate[1] - coord[1]))

    def __str__(self):
        return f"({'{:02x}'.format(self.coordinate[0])}, {'{:02x}'.format(self.coordinate[1])})"


class TileGrid():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x), self) 
            for y,x in itertools.product(range(MAPHEIGHT), range(MAPWIDTH))}

        # TODO: Make a bit more OO.
        for locations,resource in [(BERRY_LOCATIONS, Berry), 
                (TREE_LOCATIONS, Tree), (ROCK_LOCATIONS, Rocks), 
                (VEIN_LOCATIONS, Vein)]:
            for left,top,width,height in locations:
                for i,j in itertools.product(range(left,left+width), 
                                            range(top, top+height)):
                    self.grid[(i, j)].content = resource((i,j))
                    self.grid[(MAPHEIGHT - i, MAPWIDTH - j)].content = resource(
                        (MAPHEIGHT - i,MAPWIDTH - j))

    def __getitem__(self, coords: Tuple[int, int]):
        y, x = coords
        try:
            if type(y) == str:
                y = int(y, 16)
            if type(x) == str:
                x = int(x, 16)
            return self.grid[(y, x)]
        except (ValueError, KeyError):
            raise InvalidCoordinateException

    def validate_coordinate(self, *args):
        t = (args[0], args[1])
        try:
            return self.grid[t].coordinate
        except KeyError:
            raise InvalidCoordinateException












        

            








        

    


