# game.py

class Game:
    def __init__(self, room_id: str):
        self.room_id = room_id

        self.board = [
            [0] * 7
            for _ in range(6)
        ]

        self.player1 = None
        self.player2 = None

        self.turn = 1
        self.winner = None
        self.status = "waiting"

    def make_move(self, column: int):

        if column < 0 or column >= 7:
            raise ValueError("Invalid column")

        if self.winner is not None:
            raise ValueError("Game is already over")

        # Replace this with your existing board logic
        row = None

        for r in range(5, -1, -1):
            if self.board[r][column] == 0:
                row = r
                break

        if row is None:
            raise ValueError("Column is full")

        self.board[row][column] = self.turn

        # Replace this with your check_winner()
        if self.check_winner(self.turn):
            self.winner = self.turn
            self.status = "finished"
            return

        self.turn = 2 if self.turn == 1 else 1

    def check_winner(self, player: int):
        # plug your existing winner-check code in here
        return False