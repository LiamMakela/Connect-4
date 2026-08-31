type GameStatusProps = {
  winner: number | null;
  turn: number;
  status: string;
};

function GameStatus({ winner, turn, status }: GameStatusProps) {
  return (
    <div className="mb-5 text-center">
      {winner ? (
        <h2 className="text-3xl font-bold">Player {winner} wins!</h2>
      ) : status === "waiting" ? (
        <h2 className="text-xl text-slate-300">
          Waiting for another player...
        </h2>
      ) : (
        <div className="flex items-center justify-center gap-3">
          <div
            className={`w-5 h-5 rounded-full ${
              turn === 1 ? "bg-red-500" : "bg-yellow-400"
            }`}
          />

          <h2 className="text-2xl font-semibold">Player {turn}'s turn</h2>
        </div>
      )}
    </div>
  );
}

export default GameStatus;
