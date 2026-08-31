from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uuid
from app.rooms import create_game, get_game
from app.websocket_manager import manager
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/games")
def create_new_game():
    game = create_game()

    player_id = str(uuid.uuid4())

    game.player1 = player_id

    return {
        "game_id": game.room_id,
        "player_id": player_id,
        "player_number": 1
    }


@app.post("/games/{game_id}/join")
def join_game(game_id: str):
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

    game.player2 = player_id
    game.status = "playing"

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
    game = get_game(game_id)

    # Game doesn't exist
    if game is None:
        await websocket.close(code=4004)
        return

    # Player ID doesn't belong to this game
    if player_id not in [game.player1, game.player2]:
        await websocket.close(code=4003)
        return

    await manager.connect(
        game_id,
        player_id,
        websocket
    )

    # Immediately send current game state
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

            message_type = data.get("type")

            if message_type == "move":
                column = data.get("column")

                if column is None:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing column"
                    })
                    continue

                # Make sure game has started
                if game.status != "playing":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Game is not currently playing"
                    })
                    continue

                # Check whose turn it is
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

                # Try to make the move
                try:
                    game.make_move(column)

                except ValueError as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
                    continue

                # Send updated game to BOTH players
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