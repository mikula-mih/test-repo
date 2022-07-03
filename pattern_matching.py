
""" Pattern Matching """

user_input = "go_left 100".split()
action, value = user_input
print(f"{action=}, {value=}")

def run_action(user_input: int) -> None:
    if isinstance(user_input, list) and len(user_input) == 2:
        action, value = user_input
        print(f"{action=}, {value=}")
    else:
        print("Wrong command")

# Pattern Matching for Python3.10
def run_action(user_input: list) -> None:
    match user_input:
        case action, value:
            print(f"{action=}, {value=}")
        case "left", value if int(value) > 50:
            print("something ...")
        case "left" | "right" | "top" | "bottom" as action, value:
            print(f"Go to {action} to {value}px")
        case "shoot", *coords:
            print(f"Shoot by coords: {coords}")
        case "quit", :
            print("Bye")
        case _:
            print("Wrong command")


run_action("go_left 100".split())

# using dict
user_action = {
    "id": 123,
    "action": "left",
    "value": 50,
    "timestamp": 10003434,
    "user_group": 11,
    "cash": 2_000_000
}

# pattern matching checks your types
match user_action:
    case {"action": str(action), "value": int(value)}:
        print(f"{action=}, {value}")

# Using class
class UserInput:
    def __init__(self, action: str, value: int):
        self.action = action
        self.value = value

def run_horizontally(user_input: UserInput | dict):
    match user_input:
        # UserInput is not created again, just pattern matching
        case UserInput(action="left" | "right", value=value):
            print(f"Moving horizontally on {value} px")
        case {"action": "left" | "right", "value": value}:
            print(f"Moving horizontally on {value} px")
        case _:
            pass

input1 = UserInput("left", 150)
input2 = {"action": "right", "value": 300}
input3 = UserInput("top", 20)

run_horizontally(input1)
run_horizontally(input2)
run_horizontally(input3)

#
class Ok:
    __match_args__ = ("value", )
    def __init__(self, value):
        self.value = value

class Err:
    __match_args__ = ("value", )
    def __init__(self, value):
        self.value = value


Result = Ok | Err

def parse(value: str) -> Result:
    if value.isnumeric():
        return Ok(int(value))
    return Err(f"{value} is not numeric!")

match parse("123zzz"):
    case Ok(value):
        print(f"result is ok, value is {value}")
    case Err(message):
        print(f"result id error, message is {message}")
