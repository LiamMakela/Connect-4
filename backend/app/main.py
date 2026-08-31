from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import uuid

from app.rooms import create_game, get_game, save_game
from app.websocket_manager import manager


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/games")
def create_new_game():
    game = create_game()

    player_id = str(uuid.uuid4())

    game.player1 = player_id
    save_game(game)

    return {
        "game_id": game.room_id,
        "player_id": player_id,
        "player_number": 1
    }


@app.post("/games/{game_id}/join")
async def join_game(game_id: str):
    game = get_game(game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    if game.player2 is not None:
        raise HTTPException(
            status_code=400,
            detail="Game is full"
        )

    player_id = str(uuid.uuid4())

    # Update the complete game state BEFORE saving.
    game.player2 = player_id
    game.status = "playing"

    # Persist the new state to Redis.
    save_game(game)

    # Tell any already-connected player that the game has started.
    # This works because GoLoad will route all traffic for this
    # game ID to the same FastAPI instance.
    await manager.broadcast(
        game_id,
        {
            "type": "game_state",
            "board": game.board,
            "turn": game.turn,
            "winner": game.winner,
            "status": game.status,
        }
    )

    return {
        "game_id": game.room_id,
        "player_id": player_id,
        "player_number": 2
    }


@app.get("/games/{game_id}")
def get_game_state(game_id: str):
    game = get_game(game_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return {
        "game_id": game.room_id,
        "board": game.board,
        "turn": game.turn,
        "winner": game.winner,
        "status": game.status
    }


@app.websocket("/games/{game_id}/ws/{player_id}")
async def game_websocket(
    websocket: WebSocket,
    game_id: str,
    player_id: str
):
    # Always validate against the shared Redis state.
    game = get_game(game_id)

    if game is None:
        await websocket.close(code=4004)
        return

    # Player ID must belong to this game.
    if player_id not in [game.player1, game.player2]:
        await websocket.close(code=4003)
        return

    await manager.connect(
        game_id,
        player_id,
        websocket
    )

    # Send the latest state immediately after connection.
    game = get_game(game_id)

    await websocket.send_json({
        "type": "game_state",
        "board": game.board,
        "turn": game.turn,
        "winner": game.winner,
        "status": game.status
    })

    try:
        while True:
            data = await websocket.receive_json()

            # IMPORTANT:
            # Reload from Redis for every incoming action.
            #
            # Another FastAPI request may have changed this game
            # since this WebSocket originally connected.
            game = get_game(game_id)

            if game is None:
                await websocket.send_json({
                    "type": "error",
                    "message": "Game no longer exists"
                })
                continue

            message_type = data.get("type")

            if message_type == "move":
                column = data.get("column")

                if column is None:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing column"
                    })
                    continue

                # Make sure both players have joined.
                if game.status != "playing":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Game is not currently playing"
                    })
                    continue

                # Determine whose turn it currently is.
                if game.turn == 1:
                    expected_player = game.player1
                else:
                    expected_player = game.player2

                if player_id != expected_player:
                    await websocket.send_json({
                        "type": "error",
                        "message": "It is not your turn"
                    })
                    continue

                try:
                    game.make_move(column)

                    # Persist the move so every FastAPI instance
                    # has the same game state.
                    save_game(game)

                except ValueError as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
                    continue

                # Both players for this game should be connected
                # to the same FastAPI node through GoLoad's
                # consistent hashing.
                await manager.broadcast(
                    game_id,
                    {
                        "type": "game_state",
                        "board": game.board,
                        "turn": game.turn,
                        "winner": game.winner,
                        "status": game.status
                    }
                )

            elif message_type == "ping":
                await websocket.send_json({
                    "type": "pong"
                })

            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unknown message type"
                })

    except WebSocketDisconnect:
        manager.disconnect(
            game_id,
            player_id
        )