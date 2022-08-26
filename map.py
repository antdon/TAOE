from typing import List 


class Tile():
    def __init__(self, coordinate) -> None:
        self.coordinate = coordinate


class Map():
    def __init__(self) -> None:
        self.grid : List[List[Tile]] = [[Tile((a,b)) for a in range(-15, 15)] for b in range(-15,15)]


