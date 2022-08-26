from TAOE.player import Player
from TAOE.structure import Town_Hall
from map import Map
from game import Game


if __name__ == "__main__":
    map = Map()
    player = Player(Town_Hall)
    game = Game(map, player)
    while game.running:
        game.update()

