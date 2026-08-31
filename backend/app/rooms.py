# rooms.py

import random
import string

from app.game import Game


games: dict[str, Game] = {}


def generate_room_id():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


def create_game():
    room_id = generate_room_id()

    while room_id in games:
        room_id = generate_room_id()

    game = Game(room_id)

    games[room_id] = game

    return game


def get_game(room_id: str):
    return games.get(room_id)