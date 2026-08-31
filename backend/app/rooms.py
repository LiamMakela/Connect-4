import json
import os
import random
import string

import redis

from app.game import Game


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)


def generate_room_id():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


def save_game(game: Game):
    redis_client.set(
        f"game:{game.room_id}",
        json.dumps(game.to_dict())
    )


def get_game(room_id: str):
    data = redis_client.get(
        f"game:{room_id}"
    )

    if data is None:
        return None

    return Game.from_dict(
        json.loads(data)
    )


def create_game():
    room_id = generate_room_id()

    while redis_client.exists(
        f"game:{room_id}"
    ):
        room_id = generate_room_id()

    game = Game(room_id)

    save_game(game)

    return game