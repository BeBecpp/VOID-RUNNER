    # src/storage.py

import os

from src.settings import HIGHSCORE_FILE


def ensure_data_file():
    folder = os.path.dirname(HIGHSCORE_FILE)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
            file.write("0")


def load_highscore():
    ensure_data_file()

    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
            value = file.read().strip()

            if value == "":
                return 0

            return int(value)
    except (ValueError, FileNotFoundError):
        return 0


def save_highscore(score):
    ensure_data_file()

    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
        file.write(str(int(score)))