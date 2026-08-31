ROWS = 6
COLUMNS = 7
EMPTY = 0

DIRECTIONS = (
    (0, 1),   # horizontal
    (1, 0),   # vertical
    (1, 1),   # diagonal down-right
    (1, -1),  # diagonal down-left
)


class Game:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.board = [
            [EMPTY] * COLUMNS
            for _ in range(ROWS)
        ]

        self.player1 = None
        self.player2 = None

        self.turn = 1
        self.winner = None
        self.status = "waiting"

    @property
    def current_player_id(self):
        return (
            self.player1
            if self.turn == 1
            else self.player2
        )

    def make_move(self, column: int):
        if self.status != "playing":
            raise ValueError(
                "Game is not currently playing"
            )

        if (
            type(column) is not int
            or not 0 <= column < COLUMNS
        ):
            raise ValueError("Invalid column")

        row = next(
            (
                row
                for row in range(ROWS - 1, -1, -1)
                if self.board[row][column] == EMPTY
            ),
            None,
        )

        if row is None:
            raise ValueError("Column is full")

        player = self.turn
        self.board[row][column] = player

        if self.check_winner(player):
            self.winner = player
            self.status = "finished"
        elif self.is_draw():
            self.status = "finished"
        else:
            self.turn = 2 if player == 1 else 1

    def check_winner(self, player: int) -> bool:
        for row in range(ROWS):
            for column in range(COLUMNS):
                for row_step, column_step in DIRECTIONS:
                    if all(
                        0 <= row + i * row_step < ROWS
                        and 0 <= column + i * column_step < COLUMNS
                        and self.board[
                            row + i * row_step
                        ][
                            column + i * column_step
                        ] == player
                        for i in range(4)
                    ):
                        return True

        return False

    def is_draw(self) -> bool:
        return all(
            cell != EMPTY
            for cell in self.board[0]
        )

    def public_state(self):
        return {
            "board": self.board,
            "turn": self.turn,
            "winner": self.winner,
            "status": self.status,
        }

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "player1": self.player1,
            "player2": self.player2,
            **self.public_state(),
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data["room_id"])

        game.player1 = data["player1"]
        game.player2 = data["player2"]
        game.board = data["board"]
        game.turn = data["turn"]
        game.winner = data["winner"]
        game.status = data["status"]

        return game