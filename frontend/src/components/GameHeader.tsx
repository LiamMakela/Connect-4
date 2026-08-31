type GameHeaderProps = {
  gameId: string;
  playerNumber: number | null;
  status: string;
};

function GameHeader({ gameId, playerNumber, status }: GameHeaderProps) {
  return (
    <div className="w-full flex flex-wrap justify-between items-center gap-4 mb-6 bg-slate-900 border border-slate-800 rounded-2xl px-6 py-4">
      <div>
        <p className="text-slate-400 text-sm">Game Code</p>

        <p className="font-mono text-xl tracking-widest font-bold">{gameId}</p>
      </div>

      <div className="text-center">
        <p className="text-slate-400 text-sm">You are</p>

        <div className="flex items-center gap-2 font-semibold">
          <div
            className={`w-4 h-4 rounded-full ${
              playerNumber === 1 ? "bg-red-500" : "bg-yellow-400"
            }`}
          />
          Player {playerNumber}
        </div>
      </div>

      <div className="text-right">
        <p className="text-slate-400 text-sm">Status</p>

        <p className="font-semibold capitalize">{status}</p>
      </div>
    </div>
  );
}

export default GameHeader;
