export type GameState = {
  board: number[][];
  turn: number;
  winner: number | null;
  status: string;
};