import json
import redis

from app.game import Game

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def save_game(game: Game):
    redis_client.set(
        f"game:{game.room_id}",
        json.dumps(game.to_dict()),
    )


def get_game(room_id: str):
    data = redis_client.get(f"game:{room_id}")

    if data is None:
        return None

    return Game.from_dict(json.loads(data))