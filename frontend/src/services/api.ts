const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8080";

export type JoinGameResponse = {
  game_id: string;
  player_id: string;
  player_number: number;
};

export type CreateGameResponse = {
  game_id: string;
  player_id: string;
  player_number: number;
};

export async function createGame(): Promise<CreateGameResponse> {
  const response = await fetch(`${API_URL}/games`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Could not create game");
  }

  return await response.json();
}

export async function joinGame(
  gameId: string
): Promise<JoinGameResponse> {
  const response = await fetch(
    `${API_URL}/games/${gameId}/join`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    const data = await response.json();

    throw new Error(
      data.detail || "Could not join game"
    );
  }

  return await response.json();
}

export async function getGame(gameId: string) {
  const response = await fetch(
    `${API_URL}/games/${gameId}`
  );

  if (!response.ok) {
    throw new Error("Game not found");
  }

  return await response.json();
}