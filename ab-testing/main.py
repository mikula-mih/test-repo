import json
from dataclasses import dataclass
from pathlib import Path

from gui import WorsePad


@dataclass
class Config:
    show_save_button: bool = True


def read_config_file() -> Config:
    config_file = Path.cwd() / "config.json"
    config_dict = json.loads(config_file.read_text())
    return Config(**config_dict)


def main():
    config = read_config_file()
    app = WorsePad(config.show_save_button)
    app.mainloop()


if __name__ == "__main__":
    main()


'''
# with_tracking

from dotenv import load_dotenv

from event import post_event
from feature import read_config
from gui import WorsePad


def main():
    load_dotenv()
    config = read_config()
    print(config)
    app = WorsePad(post_event, config.show_save_button)
    app.mainloop()


if __name__ == "__main__":
    main()
'''
