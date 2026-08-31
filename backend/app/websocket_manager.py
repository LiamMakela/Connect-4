from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[
            str,
            dict[str, WebSocket],
        ] = {}

    async def connect(
        self,
        room_id: str,
        player_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        room = self.connections.setdefault(
            room_id,
            {},
        )

        room[player_id] = websocket

    def disconnect(
        self,
        room_id: str,
        player_id: str,
    ):
        room = self.connections.get(room_id)

        if room is None:
            return

        room.pop(player_id, None)

        if not room:
            self.connections.pop(
                room_id,
                None,
            )

    async def broadcast(
        self,
        room_id: str,
        message: dict,
    ):
        room = self.connections.get(
            room_id,
            {},
        )

        for websocket in room.values():
            await websocket.send_json(
                message
            )


manager = ConnectionManager()