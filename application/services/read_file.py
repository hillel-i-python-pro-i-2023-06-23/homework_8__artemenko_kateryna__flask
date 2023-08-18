import pathlib

from app.config import FILES_INPUT_DIR


def read_file(file_path: pathlib.Path = None):
    if file_path is None:
        file_path = FILES_INPUT_DIR.joinpath("test.txt")
    with open(file_path) as file:
        for text in file:
            print(text)
    print("")
