import { useState } from "react";
import { useNavigate } from "react-router-dom";
import GameLobby from "../components/GameLobby";
import ErrorMessage from "../components/ErrorMessage";
import { createGame, joinGame } from "../services/api";

function HomePage() {
  const [gameId, setGameId] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleCreateGame() {
    try {
      setError("");
      const data = await createGame();
      sessionStorage.setItem("playerId", data.player_id);
      sessionStorage.setItem("playerNumber", String(data.player_number));
      navigate(`/game/${data.game_id}`);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Could not create game");
      }
    }
  }

  async function handleJoinGame() {
    if (!gameId.trim()) {
      setError("Enter a game code");
      return;
    }
    try {
      setError("");
      const data = await joinGame(gameId.trim().toUpperCase());
      sessionStorage.setItem("playerId", data.player_id);
      sessionStorage.setItem("playerNumber", String(data.player_number));
      navigate(`/game/${data.game_id}`);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Could not join game");
      }
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      {" "}
      <div className="w-full max-w-lg">
        {" "}
        <div className="text-center mb-8">
          {" "}
          <h1 className="text-5xl font-bold tracking-tight">
            {" "}
            Connect 4{" "}
          </h1>{" "}
          <p className="text-slate-400 mt-2">
            {" "}
            Play online with a friend{" "}
          </p>{" "}
        </div>{" "}
        <GameLobby
          gameId={gameId}
          setGameId={setGameId}
          createGame={handleCreateGame}
          joinGame={handleJoinGame}
        />{" "}
        <ErrorMessage message={error} />{" "}
      </div>{" "}
    </div>
  );
}
export default HomePage;
