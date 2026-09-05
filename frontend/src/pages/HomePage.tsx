import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL || "";

type GameSession = {
  game_id: string;
  player_id: string;
  player_number: number;
};

async function postGame(
  path: string,
  fallbackError: string,
): Promise<GameSession> {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || fallbackError);
  }

  return response.json();
}

export default function HomePage() {
  const [gameId, setGameId] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function enterGame(path: string, fallbackError: string) {
    try {
      setError("");

      const game = await postGame(path, fallbackError);

      sessionStorage.setItem("playerId", game.player_id);
      sessionStorage.setItem("playerNumber", String(game.player_number));

      navigate(`/game/${game.game_id}`);
    } catch (error) {
      setError(error instanceof Error ? error.message : fallbackError);
    }
  }

  function joinGame() {
    const code = gameId.trim().toUpperCase();

    if (!code) {
      setError("Enter a game code");
      return;
    }

    enterGame(`/games/${code}/join`, "Could not join game");
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-lg">
        <header className="text-center mb-8">
          <h1 className="text-5xl font-bold">Connect 4</h1>
          <p className="text-slate-400 mt-2">Play online with a friend</p>
        </header>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-6">
          <button
            onClick={() => enterGame("/games", "Could not create game")}
            className="w-full bg-blue-600 hover:bg-blue-500 rounded-xl py-3 font-semibold"
          >
            Create Game
          </button>

          <div className="flex items-center gap-4">
            <div className="h-px bg-slate-700 flex-1" />
            <span className="text-slate-500 text-sm">OR</span>
            <div className="h-px bg-slate-700 flex-1" />
          </div>

          <form
            onSubmit={(event) => {
              event.preventDefault();
              joinGame();
            }}
            className="flex gap-3"
          >
            <input
              value={gameId}
              onChange={(event) => setGameId(event.target.value.toUpperCase())}
              placeholder="Enter game code"
              className="min-w-0 flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 uppercase tracking-widest"
            />

            <button
              type="submit"
              className="bg-emerald-600 hover:bg-emerald-500 rounded-xl px-6 font-semibold"
            >
              Join
            </button>
          </form>
        </div>

        {error && (
          <p className="mt-5 bg-red-950/50 border border-red-800 text-red-300 rounded-xl px-5 py-3">
            {error}
          </p>
        )}
      </div>
    </main>
  );
}
