from typing import List 
import itertools

class Tile():
    def __init__(self, coordinate) -> None:
        self.coordinate = coordinate
        self.content = None


class Map():
    def __init__(self) -> None:
        self.grid : dict[Tile] = {(y,x) : Tile((y,x)) 
            for x,y in itertools.product(range(80), repeat=2)}

        

    


