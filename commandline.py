from constants import *
from structure import LumberCamp, Mine, Mill, Barracks

class CommandLine:
    def __init__(self, screen, player):
        self.command = ""
        self.screen = screen
        self.player = player
        self.command_history = []
        self.history_pointer = 0

    def state_lookup(self, word: str):
        return {"berry": Resources.FOOD, "food": Resources.FOOD,
                "gold": Resources.GOLD, "wood": Resources.WOOD,
                "stone": Resources.STONE, "mine": Mine, "mill": Mill, 
                "lumbercamp": LumberCamp, "barracks": Barracks}.get(word, None)

    def interpret_command(self, command):
        words = command.split(" ")
        file = words[0].split("/")
        
        unit_lookup = {"archer": self.player.archers, 
                            "soldier": self.player.soldiers,
                            "cavalry": self.player.cavalry}
        # try:
        if "villager" == file[0][:8]:
            
            try:
                ind = int(file[0][8:])
                vil = self.player.villagers[ind]
            except:
                self.player.debug = f"Error! {file[0]} is not a valid villager..."
                return
            if file[1] == "gather":
                state = self.state_lookup(words[1])
                if state != None:
                    vil.set_state(VillagerStates.GATHER, state)
                    vil.update_target_square()
                    return
            if file[1] == "build":
                state = self.state_lookup(words[1])
                
                if state != None:
                    try:
                        y,x = int(words[2], 16), int(words[3], 16)
                    except ValueError:
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                cost = state.get_cost()
                if self.player.can_afford(cost):
                    vil.set_desired_square((y,x))
                    vil.set_state(VillagerStates.BUILD, state)
                else:
                    self.player.debug = read_cost("building", cost)
                return
        for unit_type, unit_container in unit_lookup.items():
            if unit_type == file[0][:len(unit_type)]:
                try:
                    self.player.debug = len(unit_container)
                    ind = int(file[0][len(unit_type):])
                    chosen_unit = unit_container[ind]
                except:
                    if file[0][len(unit_type):] == "s":
                        if file[1] == "attack":
                            for u in unit_container:
                                if words[1] == "soldier":
                                    u.set_attacking(Units.SOLDIER)
                                if words[1] == "archer":
                                    u.set_attacking(Units.ARCHER)
                                if words[1] == "cavalry":
                                    u.set_attacking(Units.CAVALRY)
                                if words[1] == "villager":
                                    u.set_attacking(Units.VILLAGER)
                            return
                    else:
                        self.player.debug = f"Error! {file[0]} is not a valid {unit_type}"
                        return
                if file[1] == "move":
                    try:
                        y,x = int(words[1], 16), int(words[2], 16)
                        if (y,x) not in self.player.game.grid.grid:
                            raise KeyError
                    except (ValueError, KeyError):
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                    chosen_unit.state_action = ArmyStates.MOVE
                    chosen_unit.state_target = None
                    chosen_unit.set_desired_square((y,x))
                    return
                if file[1] == "attack":
                    if words[1] == "soldier":
                        chosen_unit.set_attacking(Units.SOLDIER)
                    if words[1] == "archer":
                        chosen_unit.set_attacking(Units.ARCHER)
                    if words[1] == "cavalry":
                        chosen_unit.set_attacking(Units.CAVALRY)
                    if words[1] == "villager":
                        chosen_unit.set_attacking(Units.VILLAGER)
        if command == "townhall/create villager":
            self.player.structures[0].create_villager()
        elif command == "barracks/create soldier":
            self.player.get_barracks().create_soldier()
        elif command == "barracks/create archer":
            self.player.get_barracks().create_archer()
        elif command == "barracks/create cavalry":
            self.player.get_barracks().create_cavalry()
        elif command == "townhall/create soldier":
            self.player.debug = "You build those at a barracks."
        elif command == "townhall/create archer":
            self.player.debug = "You build those at a barracks."
        elif command == "townhall/create cavalry":
            self.player.debug = "You build those at a barracks."
        # except:
        #     self.player.debug = "I don't understand."

    def set_history_pointer(self, target: int):
        self.history_pointer = max(0, min(target, len(self.command_history)))

    def get_command_at_pointer(self):
        try:
            return self.command_history[self.history_pointer]
        except IndexError:
            return ""

    def clear_command(self):
        self.set_history_pointer(len(self.command_history))
        self.command = self.get_command_at_pointer()

    def update(self, newkey):
        if newkey == 263:
            self.command = self.command[:-1]
        elif newkey == 10:
            self.command_history.append(self.command)
            for command in self.command.split(";"):
                self.interpret_command(command.strip())
            self.clear_command()
        elif newkey == 27:
            self.clear_command()
        elif newkey == 259:
            self.set_history_pointer(self.history_pointer - 1)
            self.command = self.get_command_at_pointer()
        elif newkey == 258:
            self.set_history_pointer(self.history_pointer + 1)
            self.command = self.get_command_at_pointer()
        elif newkey == 9:
            self.player.game.switch_players()
        else:
            self.command += chr(newkey)
        self.draw()

    def draw(self):
        self.player.screen.addstr(COMMANDLINE_Y, 0, " "*100)
        self.player.screen.addstr(COMMANDLINE_Y, 0, self.command)