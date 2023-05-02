
""" Plugin Architecture """
# allows you to add functionality to an application without changing a single
# line in the original code

# Basic example showing how to create objects from data using a dynamic factory
# with register/unregister methods;

import json
import os
from dataclasses import dataclass

from game import factory, loader

os.chdir(
    os.path.dirname(__file__)
)

@dataclass
class Sorcerer:

    name: str

    def make_a_noise(self) -> None:
        print("Aaaargh!")

@dataclass
class Wizard:

    name: str

    def make_a_noise(self) -> None:
        print("Boohh!")

@dataclass
class Witcher:

    name: str

    def make_a_noise(self) -> None:
        print("Hmmm")

def main() -> None:
    """Creates game characters from a file containing a level definition."""

    # register a couple of character types
    factory.register("sorcerer", Sorcerer)
    factory.register("wizard", Wizard)
    factory.register("witcher", Witcher)

    # read data from a JSON file
    with open("./level.json") as file:
        data = json.load(file)

        # load the plugins
        loader.load_plugins(data["plugins"])

        # create the characters
        characters = [factory.create(item) for item in data["characters"]]

        # do something with the characters
        for character in characters:
            print(character, end="\t")
            character.make_a_noise()

if __name__ == "__main__":
    main()
