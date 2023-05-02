import os.path
import pathlib


def analyze_data(file: str):
    if not os.path.exists(file):
        print(f"Does not exist, exiting: {file}")
        return
    # FILE DELETED?
    with open(file) as fp: # RAISES FileNotFoundError
        data = fp.read()
        ... # analyze the data

    # better use try: except:
    try:
        # data = pathlib.Path(file).read_text()
        with open(file) as fp:
            data = fp.read()
            ...
    except FileNotFoundError:
        print(f"Does not exist, exiting: {file}")
        return
    except IsADirectoryError:
        ...

def initialize_app():
    config_dir = "."
    if is_user_config_dir_present(config_dir):
        ... # load config files
    else:
        ... # load defaults

def your_options():
    file = "path/to/some/file.txt"
    # path = pathlib.Path(file)
    # if os.path.isdir(file):
    if os.path.exists(file):
        print("Found")
    else:
        print("Not found")

    path = pathlib.Path("path", "to", "some", "file.txt")
    if path.exists():
        print("Found")
    else:
        print("Not found")

    # path.exists() -> os.path.exists(path)
    # path.is_file() -> os.path.isfile(path)
    # path.is_dir() -> os.path.isdir(path)
