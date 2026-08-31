type GameLobbyProps = {
  gameId: string;
  setGameId: (gameId: string) => void;
  createGame: () => void;
  joinGame: () => void;
};

function GameLobby({
  gameId,
  setGameId,
  createGame,
  joinGame,
}: GameLobbyProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl p-8">
      <div className="flex flex-col gap-6">
        <button
          onClick={createGame}
          className="w-full bg-blue-600 hover:bg-blue-500 transition rounded-xl py-3 font-semibold text-lg"
        >
          Create Game
        </button>

        <div className="flex items-center gap-4">
          <div className="h-px bg-slate-700 flex-1" />

          <span className="text-slate-500 text-sm">OR</span>

          <div className="h-px bg-slate-700 flex-1" />
        </div>

        <div className="flex gap-3">
          <input
            value={gameId}
            onChange={(e) => setGameId(e.target.value.toUpperCase())}
            placeholder="Enter game code"
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-blue-500 uppercase tracking-widest"
          />

          <button
            onClick={joinGame}
            className="bg-emerald-600 hover:bg-emerald-500 transition rounded-xl px-6 font-semibold"
          >
            Join
          </button>
        </div>
      </div>
    </div>
  );
}

export default GameLobby;
