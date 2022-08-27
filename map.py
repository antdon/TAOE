from typing import List 
import itertools

from incidental import Tree

class Tile:
    def __init__(self, coordinate) -> None:
        self.coordinate = coordinate
        self.content = None

    def get_dist(self, coord: tuple[int, int]) -> int:
        return max(abs(self.coordinate[0] - coord[0]), abs(self.coordinate[1] - coord[1]))


class Map():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x)) 
            for x,y in itertools.product(range(80), repeat=2)}

        for index, tile in enumerate(self.grid.values()):
            if index % 7 == 0: 
                tile.content = Tree(tile.coordinate)


        

            








        

    


