import type { GameState } from "../types/game";

const WS_URL =
  import.meta.env.VITE_WS_URL ||
  "ws://localhost:8080";

export type GameMessage =
  | ({
      type: "game_state";
    } & GameState)
  | {
      type: "error";
      message: string;
    }
  | {
      type: "pong";
    };

export function createGameSocket(
  gameId: string,
  playerId: string,
  onMessage: (message: GameMessage) => void,
  onClose?: () => void
): WebSocket {
  const socket = new WebSocket(
    `${WS_URL}/games/${gameId}/ws/${playerId}`
  );

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    const message: GameMessage =
      JSON.parse(event.data);

    onMessage(message);
  };

  socket.onerror = (error) => {
    console.error(
      "WebSocket error:",
      error
    );
  };

  socket.onclose = () => {
    console.log(
      "WebSocket disconnected"
    );

    if (onClose) {
      onClose();
    }
  };

  return socket;
}

export function sendMove(
  socket: WebSocket,
  column: number
) {
  if (
    socket.readyState !== WebSocket.OPEN
  ) {
    return;
  }

  socket.send(
    JSON.stringify({
      type: "move",
      column,
    })
  );
}

export function sendPing(
  socket: WebSocket
) {
  if (
    socket.readyState !== WebSocket.OPEN
  ) {
    return;
  }

  socket.send(
    JSON.stringify({
      type: "ping",
    })
  );
}