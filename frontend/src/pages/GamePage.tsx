import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import GameBoard from "../components/GameBoard";
import GameHeader from "../components/GameHeader";
import GameStatus from "../components/GameStatus";
import ErrorMessage from "../components/ErrorMessage";
import { createGameSocket, sendMove } from "../services/websocket";
import type { GameMessage } from "../services/websocket";
import type { GameState } from "../types/game";

function GamePage() {
  const { gameId } = useParams();
  const navigate = useNavigate();
  const playerId = sessionStorage.getItem("playerId");
  const storedPlayerNumber = sessionStorage.getItem("playerNumber");
  const playerNumber =
    storedPlayerNumber !== null ? Number(storedPlayerNumber) : null;
  const [game, setGame] = useState<GameState>({
    board: Array.from({ length: 6 }, () => Array(7).fill(0)),
    turn: 1,
    winner: null,
    status: "connecting",
  });
  const [error, setError] = useState("");
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!gameId || !playerId) {
      navigate("/");
      return;
    }

    function handleMessage(message: GameMessage) {
      if (message.type === "game_state") {
        setGame({
          board: message.board,
          turn: message.turn,
          winner: message.winner,
          status: message.status,
        });
        setError("");
      }
      if (message.type === "error") {
        setError(message.message);
      }
    }

    const socket = createGameSocket(gameId, playerId, handleMessage, () => {
      setError("Disconnected from game");
    });
    socketRef.current = socket;
    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [gameId, playerId, navigate]);

  function handlePlayColumn(column: number) {
    if (!socketRef.current) {
      setError("Not connected to server");
      return;
    }
    sendMove(socketRef.current, column);
  }

  function handleLeaveGame() {
    if (socketRef.current) {
      socketRef.current.close();
    }
    sessionStorage.removeItem("playerId");
    sessionStorage.removeItem("playerNumber");
    navigate("/");
  }
  if (!gameId) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      {" "}
      <div className="w-full max-w-3xl flex flex-col items-center">
        {" "}
        <div className="text-center mb-8">
          {" "}
          <h1 className="text-4xl font-bold tracking-tight">
            {" "}
            Connect 4{" "}
          </h1>{" "}
        </div>{" "}
        <GameHeader
          gameId={gameId}
          playerNumber={playerNumber}
          status={game.status}
        />{" "}
        <GameStatus
          winner={game.winner}
          turn={game.turn}
          status={game.status}
        />{" "}
        <GameBoard board={game.board} playColumn={handlePlayColumn} />{" "}
        <ErrorMessage message={error} />{" "}
        <button
          onClick={handleLeaveGame}
          className="mt-8 text-slate-400 hover:text-white transition"
        >
          {" "}
          Leave Game{" "}
        </button>{" "}
      </div>{" "}
    </div>
  );
}
export default GamePage;
