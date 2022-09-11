class InvalidCommandException(Exception):
    message = "Sorry, I don't understand."

class InvalidCoordinateException(InvalidCommandException):
    message = "Invalid coordinates! (Remember row first)"

class InvalidUnitArgumentException(InvalidCommandException):
    message = "I don't understand what the target is."

class WrongBuildingException(InvalidCommandException):
    def __init__(self, building):
        self.message = f"You build those at a {building}."

class InvalidResourceTypeException(InvalidCommandException):
    message = "I don't recognise that resource name."

class InvalidBuildingTypeException(InvalidCommandException):
    message = "I don't recognise that building name."

class InvalidCommandArgumentException(InvalidCommandException):
    message = "I don't recognise one of the arguments in your command."

class InvalidUnitTypeException(InvalidCommandException):
    message = "I don't recognise that unit type."

    def __init__(self, attempted_name, unit_type):
        self.message = f"Error! {attempted_name} is not a valid {unit_type}..."

class InsufficientFundsException(InvalidCommandException):
    def __init__(self, message):
        self.message = message