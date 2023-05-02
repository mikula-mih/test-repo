from datetime import datetime
from functools import partial
from typing import Callable

""" 3 Simple Ideas from Functional Programming for your Code Imporovement """

# Object-Oriented Programming and Functional programming are part of two completely
# different paradigms:
#   - Imperative: focuses on how to execute; it defines control flow as statements
#       that change a program's state; `algorithmic programming`
#   - Declarative: focuses on what to execute; it defines program logic but not a
#       detailed control flow; `functional programming` is a programming paradigm
#       where programs are constructed by applying and composing functions;

def OOP_v1() -> None:

    class Greeting:
        def __init__(self) -> None:
            current_time = datetime.now()
            if current_time.hour < 12:
                self.greeting_intro = "Good morning"
            elif 12 <= current_time.hour < 18:
                self.greeting_intro = "Good afternoon"
            else:
                self.greeting_intro = "Good evening"

        def greet(self, name: str) -> None:
            print(f"{self.greeting_intro}, {name}.")

        def greet_list(self, names: list[str]) -> None:
            for name in names:
                self.greet(name)

    name = input("Enter your name: ")

    greeting = Greeting()
    greeting.greet(name)


def OOP_v2() -> None:

    class Greeting:
        def __init__(self, greeting_intro: str) -> None:
            self.greeting_intro = greeting_intro

        def greet(self, name: str) -> str:
            return f"{self.greeting_intro}, {name}."

        def greet_list(self, names: list[str]) -> list[str]:
            greetings: list[str] = []
            for name in names:
                greetings.append(self.greet(name))
            return greetings


    current_time = datetime.now()
    if current_time.hour < 12:
        greeting_intro = "Good morning"
    elif 12 <= current_time.hour < 18:
        greeting_intro = "Good afternoon"
    else:
        greeting_intro = "Good evening"

    name = input("Enter your name: ")

    greeting = Greeting(greeting_intro)
    print(greeting.greet(name))
    print("\n".join(greeting.greet_list(["John", "Jane", "Joe"])))

# `Side effect`: is when a function or method relies on or modify something
#       on the outside of that funciton: pringting smth, reading from a file,
#       writing to a file, interacting with a database, interacting with other
#       services;
#       Side effects make your code hard to maintain and make things harder to
#       test because you can't isolate a functional or method properly;
# `Pure function`: if a function doesn't have side effects and the return value
#       is only determined by its input values;
# `Functions are first-class citizens`: they are not just groups of statements with
#       input arguments and return value there are things that you can compose,
#       deconstruct, pass to other funcitons, and return as a value to a function;
#       if a function receives a function as an argument or it returns a funciton
#       as a result it's called a `higher order function`;
# In imperative languages like Python variables can be accessed or changed anytime
# you like; in declarative variables are generally bound to expressions and keep
# a single value during their entire lifetime;

def Func_v1():

    def greet(name: str, greeting_intro: str) -> str:
        return f"{greeting_intro}, {name}."

    def greet_list(names: list[str], greeting_intro: str) -> list[str]:
        return [greet(name, greeting_intro) for name in names]

    def read_greeting() -> str:
        current_time = datetime.now()
        if current_time.hour < 12:
            return "Good morning"
        elif 12 <= current_time.hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def read_name() -> str:
        return input("Enter your name: ")


    print(greet(read_name(), read_greeting()))
    print(greet_list(["John", "Jane", "Joe"], read_greeting()))


def Func_v2():

    GreetingReader = Callable[[], str]

    def greet(name: str, greeting_reader: GreetingReader) -> str:
        if name == "Arjan":
            return "Bugger off"
        return f"{greeting_reader()}, {name}."

    def greet_list(names: list[str], greeting_reader: GreetingReader) -> list[str]:
        return [greet(name, greeting_reader) for name in names]

    def read_greeting() -> str:
        current_time = datetime.now()
        if current_time.hour < 12:
            return "Good morning"
        elif 12 <= current_time.hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def read_name() -> str:
        return input("Enter your name: ")


    print(greet(read_name(), read_greeting))
    print(greet_list(["John", "Jane", "Joe"], read_greeting))


def Func_v3():

    GreetingReader = Callable[[], str]
    GreetingFunction = Callable[[str], str]

    def greet(name: str, greeting_reader: GreetingReader) -> str:
        if name == "Arjan":
            return "Bugger off"
        return f"{greeting_reader()}, {name}."

    def greet_list(names: list[str], greet_fn: GreetingFunction) -> list[str]:
        return [greet_fn(name) for name in names]

    def read_greeting() -> str:
        current_time = datetime.now()
        if current_time.hour < 12:
            return "Good morning"
        elif 12 <= current_time.hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def read_name() -> str:
        return input("Enter your name: ")


    greet_fn = partial(greet, greeting_reader=read_greeting)
    print(greet_fn(read_name()))
    print("\n".join(greet_list(["John", "Jane", "Joe"], greet_fn)))


def immutable_examples():
    import random

    test_list = [120, 68, -20, 0, 5, 67, 14, 99]

    # built in immutable sort
    sorted_list = sorted(test_list)
    print(f"Original list: {test_list}")
    print(f"Sorted list: {sorted_list}")

    # built in mutable sort
    test_list.sort()
    print(f"Original list: {test_list}")

    # other example of mutable vs immutable operations
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    shuffled_cards = random.sample(cards, k=len(cards))
    print(f"Shuffled cards: {shuffled_cards}")
    print(f"Original cards: {cards}")

    random.shuffle(cards)  # shuffles the cards (mutable)
    print(f"Cards: {cards}")


if __name__ == "__main__":
    # OOP_v1()
    # OOP_v2()
    # Func_v1()
    # Func_v2()
    # Func_v3()
    immutable_examples()
