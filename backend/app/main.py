import os
from uuid import uuid4

from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.game import Game
from app.rooms import (
    create_game,
    get_game,
    save_game,
)
from app.websocket_manager import manager


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv(
            "FRONTEND_ORIGIN",
            "http://localhost:5173",
        )
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def new_player_id() -> str:
    return str(uuid4())


def game_message(game: Game):
    return {
        "type": "game_state",
        **game.public_state(),
    }


def require_game(game_id: str) -> Game:
    game = get_game(game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    return game


async def send_error(
    websocket: WebSocket,
    message: str,
):
    await websocket.send_json({
        "type": "error",
        "message": message,
    })


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/games")
def create_new_game():
    player_id = new_player_id()
    game = create_game(player_id)

    return {
        "game_id": game.room_id,
        "player_id": player_id,
        "player_number": 1,
    }


@app.post("/games/{game_id}/join")
async def join_game(game_id: str):
    game = require_game(game_id)

    if game.player2 is not None:
        raise HTTPException(
            status_code=400,
            detail="Game is full",
        )

    player_id = new_player_id()

    game.player2 = player_id
    game.status = "playing"

    save_game(game)

    await manager.broadcast(
        game_id,
        game_message(game),
    )

    return {
        "game_id": game.room_id,
        "player_id": player_id,
        "player_number": 2,
    }


@app.get("/games/{game_id}")
def get_game_state(game_id: str):
    game = require_game(game_id)

    return {
        "game_id": game.room_id,
        **game.public_state(),
    }


@app.websocket(
    "/games/{game_id}/ws/{player_id}"
)
async def game_websocket(
    websocket: WebSocket,
    game_id: str,
    player_id: str,
):
    game = get_game(game_id)

    if game is None:
        await websocket.close(code=4004)
        return

    if player_id not in (
        game.player1,
        game.player2,
    ):
        await websocket.close(code=4003)
        return

    await manager.connect(
        game_id,
        player_id,
        websocket,
    )

    await websocket.send_json(
        game_message(game)
    )

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "ping":
                await websocket.send_json({
                    "type": "pong"
                })
                continue

            if message_type != "move":
                await send_error(
                    websocket,
                    "Unknown message type",
                )
                continue

            # Redis is the source of truth.
            game = get_game(game_id)

            if game is None:
                await websocket.close(
                    code=4004
                )
                return

            if game.status != "playing":
                await send_error(
                    websocket,
                    "Game is not currently playing",
                )
                continue

            if (
                player_id
                != game.current_player_id
            ):
                await send_error(
                    websocket,
                    "It is not your turn",
                )
                continue

            try:
                game.make_move(
                    data.get("column")
                )
            except ValueError as error:
                await send_error(
                    websocket,
                    str(error),
                )
                continue

            save_game(game)

            await manager.broadcast(
                game_id,
                game_message(game),
            )

    except WebSocketDisconnect:
        manager.disconnect(
            game_id,
            player_id,
        )