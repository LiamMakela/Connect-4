import json
import os
import random
import string

import redis

from app.game import Game


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


def game_key(room_id: str) -> str:
    return f"game:{room_id}"


def generate_room_id() -> str:
    characters = (
        string.ascii_uppercase
        + string.digits
    )

    return "".join(
        random.choices(characters, k=6)
    )


def save_game(game: Game):
    redis_client.set(
    game_key(game.room_id),
    json.dumps(game.to_dict()),
    ex=86400,
    )


def get_game(room_id: str):
    data = redis_client.get(
        game_key(room_id)
    )

    if data is None:
        return None

    return Game.from_dict(
        json.loads(data)
    )


def create_game(player1_id: str):
    while True:
        room_id = generate_room_id()

        if not redis_client.exists(
            game_key(room_id)
        ):
            break

    game = Game(room_id)
    game.player1 = player1_id

    save_game(game)

    return game