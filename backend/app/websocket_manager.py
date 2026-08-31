# websocket_manager.py

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # {
        #   "ROOM1": {
        #       "player-id-1": websocket,
        #       "player-id-2": websocket
        #   }
        # }
        self.connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(
        self,
        room_id: str,
        player_id: str,
        websocket: WebSocket
    ):
        await websocket.accept()

        if room_id not in self.connections:
            self.connections[room_id] = {}

        self.connections[room_id][player_id] = websocket

    def disconnect(self, room_id: str, player_id: str):
        if room_id not in self.connections:
            return

        self.connections[room_id].pop(player_id, None)

        if len(self.connections[room_id]) == 0:
            del self.connections[room_id]

    async def send_to_player(
        self,
        room_id: str,
        player_id: str,
        message: dict
    ):
        if room_id not in self.connections:
            return

        websocket = self.connections[room_id].get(player_id)

        if websocket:
            await websocket.send_json(message)

    async def broadcast(self, room_id: str, message: dict):
        if room_id not in self.connections:
            return

        for websocket in self.connections[room_id].values():
            await websocket.send_json(message)


manager = ConnectionManager()