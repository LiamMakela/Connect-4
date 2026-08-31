import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8080";

type GameState = {
  board: number[][];
  turn: number;
  winner: number | null;
  status: string;
};

type GameMessage =
  | ({ type: "game_state" } & GameState)
  | { type: "error"; message: string }
  | { type: "pong" };

const initialGame: GameState = {
  board: Array.from({ length: 6 }, () => Array(7).fill(0)),
  turn: 1,
  winner: null,
  status: "connecting",
};

function playerColor(player: number | null) {
  if (player === 1) return "bg-red-500";
  if (player === 2) return "bg-yellow-400";
  return "bg-slate-600";
}

export default function GamePage() {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const socketRef = useRef<WebSocket | null>(null);

  const playerId = sessionStorage.getItem("playerId");

  const playerNumber = Number(sessionStorage.getItem("playerNumber")) || null;

  const [game, setGame] = useState<GameState>(initialGame);

  const [error, setError] = useState("");

  useEffect(() => {
    if (!gameId || !playerId) {
      navigate("/", { replace: true });
      return;
    }

    const socket = new WebSocket(`${WS_URL}/games/${gameId}/ws/${playerId}`);

    socketRef.current = socket;

    socket.onmessage = (event) => {
      const message: GameMessage = JSON.parse(event.data);

      if (message.type === "game_state") {
        setGame(message);
        setError("");
      }

      if (message.type === "error") {
        setError(message.message);
      }
    };

    socket.onclose = () => {
      if (socketRef.current === socket) {
        setError("Disconnected from game");
      }
    };

    return () => {
      socketRef.current = null;
      socket.close();
    };
  }, [gameId, playerId, navigate]);

  function playColumn(column: number) {
    const socket = socketRef.current;

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      setError("Not connected to server");
      return;
    }

    socket.send(
      JSON.stringify({
        type: "move",
        column,
      }),
    );
  }

  function leaveGame() {
    socketRef.current?.close();
    socketRef.current = null;

    sessionStorage.removeItem("playerId");
    sessionStorage.removeItem("playerNumber");

    navigate("/");
  }

  if (!gameId || !playerId) {
    return null;
  }

  const statusText = game.winner
    ? `Player ${game.winner} wins!`
    : game.status === "waiting"
      ? "Waiting for another player..."
      : game.status === "connecting"
        ? "Connecting..."
        : game.status === "finished"
          ? "Draw!"
          : `Player ${game.turn}'s turn`;

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-3xl flex flex-col items-center">
        <h1 className="text-4xl font-bold mb-8">Connect 4</h1>

        <div className="w-full flex justify-between items-center gap-4 mb-6 bg-slate-900 border border-slate-800 rounded-2xl px-6 py-4">
          <div>
            <p className="text-sm text-slate-400">Game Code</p>
            <p className="font-mono text-xl font-bold tracking-widest">
              {gameId}
            </p>
          </div>

          <div className="text-center">
            <p className="text-sm text-slate-400">You are</p>

            <div className="flex items-center gap-2 font-semibold">
              <span
                className={`w-4 h-4 rounded-full ${playerColor(playerNumber)}`}
              />
              Player {playerNumber}
            </div>
          </div>

          <div className="text-right">
            <p className="text-sm text-slate-400">Status</p>
            <p className="font-semibold capitalize">{game.status}</p>
          </div>
        </div>

        <div className="flex items-center gap-3 mb-5">
          {!game.winner && game.status === "playing" && (
            <span
              className={`w-5 h-5 rounded-full ${playerColor(game.turn)}`}
            />
          )}

          <h2 className="text-2xl font-semibold">{statusText}</h2>
        </div>

        <div className="grid grid-cols-7 gap-2 bg-blue-700 p-4 rounded-3xl shadow-2xl">
          {game.board.map((row, rowIndex) =>
            row.map((cell, columnIndex) => (
              <button
                key={`${rowIndex}-${columnIndex}`}
                onClick={() => playColumn(columnIndex)}
                className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-slate-950 flex items-center justify-center hover:ring-4 hover:ring-blue-400/50"
              >
                {cell !== 0 && (
                  <span
                    className={`w-11 h-11 sm:w-13 sm:h-13 rounded-full ${playerColor(cell)}`}
                  />
                )}
              </button>
            )),
          )}
        </div>

        {error && (
          <p className="mt-5 bg-red-950/50 border border-red-800 text-red-300 rounded-xl px-5 py-3">
            {error}
          </p>
        )}

        <button
          onClick={leaveGame}
          className="mt-8 text-slate-400 hover:text-white"
        >
          Leave Game
        </button>
      </div>
    </main>
  );
}
