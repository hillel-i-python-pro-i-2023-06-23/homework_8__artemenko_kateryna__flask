import pathlib
from typing import Final

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent.parent
FILES_INPUT_DIR: Final[pathlib.Path] = ROOT_DIR.joinpath("files_input")
DB_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath("db", "db_sqlite")
