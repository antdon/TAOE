from typing import List 
import itertools

from incidental import Berry, Tree, Vein

class Tile:
    def __init__(self, coordinate, tilemap) -> None:
        self.coordinate = coordinate
        self.tilemap = tilemap
        self.content = None

    def get_neighbours(self):
        squares = []
        for y,x in itertools.product(range(-1,2),repeat=2):
            if y == x == 0:
                pass
            else:
                squares.append(self.tilemap.grid[(self.coordinate[0]+y, self.coordinate[1]+x)])
        return squares

    def get_dist(self, coord: tuple[int, int]) -> int:
        return max(abs(self.coordinate[0] - coord[0]), abs(self.coordinate[1] - coord[1]))


class Map():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x), self) 
            for x,y in itertools.product(range(80), repeat=2)}
        for i in range(20,29):
            for j in range(47,57):
                self.grid[(i, j)].content = Tree((i,j))

        for i in range(0, 11):
            for j in range(4,13):
                self.grid[(i, j)].content = Berry((i,j))

        for i in range(35, 40):
            for j in range(24, 30):
                self.grid[(i, j)].content = Vein((i,j))











        

            








        

    


