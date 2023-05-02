
""" Adapter Design Pattern """
# the goal of the adapter pattern is to adapt an existing system so you can use
# it in your application; you can do this by creating a layer that's called
# the adapter between that existing systme and your own code;
# two versions of pattern:
# object-based version & class-based version
# In object-based version you're relying on composition;
import json
import os
from bs4 import BeautifulSoup

from experiment import Experiment
from xml_adapter import XMLConfig

os.chdir(
    os.path.dirname(__file__)
)

def main() -> None:
    with open("config.json", encoding="utf8") as file:
        config = json.load(file)
    experiment = Experiment(config)
    experiment.run()

if __name__ == "__main__":
    main()
