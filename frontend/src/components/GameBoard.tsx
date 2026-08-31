type GameBoardProps = {
  board: number[][];
  playColumn: (column: number) => void;
};

function GameBoard({ board, playColumn }: GameBoardProps) {
  return (
    <div className="bg-blue-700 p-4 rounded-3xl shadow-2xl">
      <div className="grid grid-cols-7 gap-2">
        {board.map((row, rowIndex) =>
          row.map((cell, columnIndex) => (
            <button
              key={`${rowIndex}-${columnIndex}`}
              onClick={() => playColumn(columnIndex)}
              className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-slate-950 flex items-center justify-center hover:ring-4 hover:ring-blue-400/50 transition"
            >
              {cell === 1 && (
                <div className="w-11 h-11 sm:w-13 sm:h-13 rounded-full bg-red-500 shadow-inner" />
              )}

              {cell === 2 && (
                <div className="w-11 h-11 sm:w-13 sm:h-13 rounded-full bg-yellow-400 shadow-inner" />
              )}
            </button>
          )),
        )}
      </div>
    </div>
  );
}

export default GameBoard;
