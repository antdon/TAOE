from typing import List 
import itertools

from incidental import Berry, Tree, Vein

class Tile():
    def __init__(self, coordinate) -> None:
        self.coordinate = coordinate
        self.content = None


class Map():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x)) 
            for x,y in itertools.product(range(80), repeat=2)}


        for i in range(20,29):
            for j in range(47,57):
                self.grid[(i, j)].content = Tree((i,j))

        for i in range(0, 11):
            for j in range(4,13):
                self.grid[(i, j)].content = Berry((i,j))

        for i in range(35, 40):
            for j in range(24, 30):
                self.grind[(i, j)].content = Vein((i,j))











        

            








        

    


