class InvalidCommandException(Exception):
    message = "Sorry, I don't understand."

class InvalidCoordinateException(Exception):
    message = "Invalid coordinates! (Remember row first)"

class InvalidUnitArgumentException(Exception):
    message = "I don't understand what the target is."

class WrongBuildingException(Exception):
    def __init__(self, building):
        self.message = f"You build those at a {building}."

class InvalidResourceTypeException(Exception):
    message = "I don't recognise that resource name."

class InvalidBuildingTypeException(Exception):
    message = "I don't recognise that building name."

class InvalidCommandArgumentException(Exception):
    message = "I don't recognise one of the arguments in your command."

class InvalidUnitTypeException(Exception):
    message = "I don't recognise that unit type."

    def __init__(self, attempted_name, unit_type):
        self.message = f"Error! {attempted_name} is not a valid {unit_type}..."

class InsufficientFundsException(Exception):
    def __init__(self, message):
        self.message = message