class Game:
    ROWS = 6
    COLUMNS = 7

    def __init__(self, room_id: str):
        self.room_id = room_id

        self.board = [
            [0] * self.COLUMNS
            for _ in range(self.ROWS)
        ]

        self.player1 = None
        self.player2 = None

        self.turn = 1
        self.winner = None
        self.status = "waiting"

    def make_move(self, column: int):
        if self.status != "playing":
            raise ValueError("Game is not currently playing")

        if column < 0 or column >= self.COLUMNS:
            raise ValueError("Invalid column")

        if self.winner is not None:
            raise ValueError("Game is already over")

        row = None

        # Start at the bottom and find the first empty slot.
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][column] == 0:
                row = r
                break

        if row is None:
            raise ValueError("Column is full")

        player = self.turn

        self.board[row][column] = player

        if self.check_winner(row, column, player):
            self.winner = player
            self.status = "finished"
            return

        if self.is_draw():
            self.status = "finished"
            return

        self.turn = 2 if self.turn == 1 else 1

    def check_winner(
        self,
        row: int,
        column: int,
        player: int
    ) -> bool:
        """
        Check all four possible Connect-4 directions:

        horizontal
        vertical
        diagonal \
        diagonal /
        """

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for row_direction, column_direction in directions:
            count = 1

            # Look in the positive direction.
            count += self._count_direction(
                row,
                column,
                row_direction,
                column_direction,
                player,
            )

            # Look in the negative direction.
            count += self._count_direction(
                row,
                column,
                -row_direction,
                -column_direction,
                player,
            )

            if count >= 4:
                return True

        return False

    def _count_direction(
        self,
        row: int,
        column: int,
        row_direction: int,
        column_direction: int,
        player: int
    ) -> int:
        count = 0

        current_row = row + row_direction
        current_column = column + column_direction

        while (
            0 <= current_row < self.ROWS
            and 0 <= current_column < self.COLUMNS
            and self.board[current_row][current_column] == player
        ):
            count += 1

            current_row += row_direction
            current_column += column_direction

        return count

    def is_draw(self) -> bool:
        """
        The board is full if every cell in the top row
        contains a piece.
        """
        return all(
            self.board[0][column] != 0
            for column in range(self.COLUMNS)
        )

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "board": self.board,
            "player1": self.player1,
            "player2": self.player2,
            "turn": self.turn,
            "winner": self.winner,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data["room_id"])

        game.board = data["board"]
        game.player1 = data["player1"]
        game.player2 = data["player2"]
        game.turn = data["turn"]
        game.winner = data["winner"]
        game.status = data["status"]

        return game