from app.game import Game


def create_started_game():
    game = Game("TEST01")
    game.player1 = "player-1"
    game.player2 = "player-2"
    game.status = "playing"

    return game


def test_horizontal_win():
    game = create_started_game()

    moves = [
        0, 0,
        1, 1,
        2, 2,
        3,
    ]

    for column in moves:
        game.make_move(column)

    assert game.winner == 1
    assert game.status == "finished"


def test_vertical_win():
    game = create_started_game()

    moves = [
        0, 1,
        0, 1,
        0, 1,
        0,
    ]

    for column in moves:
        game.make_move(column)

    assert game.winner == 1
    assert game.status == "finished"


def test_diagonal_win():
    game = create_started_game()

    moves = [
        0, 1,
        1, 2,
        4, 2,
        2, 3,
        4, 3,
        5, 3,
        3,
    ]

    for column in moves:
        game.make_move(column)

    assert game.winner == 1
    assert game.status == "finished"


def test_turn_switches():
    game = create_started_game()

    assert game.turn == 1

    game.make_move(0)

    assert game.turn == 2

    game.make_move(1)

    assert game.turn == 1


def test_piece_falls_to_bottom():
    game = create_started_game()

    game.make_move(3)

    assert game.board[5][3] == 1


def test_pieces_stack():
    game = create_started_game()

    game.make_move(3)
    game.make_move(3)

    assert game.board[5][3] == 1
    assert game.board[4][3] == 2


def test_invalid_column():
    game = create_started_game()

    try:
        game.make_move(10)
        assert False
    except ValueError as error:
        assert str(error) == "Invalid column"


def test_full_column():
    game = create_started_game()

    for _ in range(6):
        game.make_move(0)

    try:
        game.make_move(0)
        assert False
    except ValueError as error:
        assert str(error) == "Column is full"


def test_serialization_round_trip():
    game = create_started_game()

    game.make_move(3)
    game.make_move(4)

    data = game.to_dict()

    restored = Game.from_dict(data)

    assert restored.room_id == game.room_id
    assert restored.board == game.board
    assert restored.turn == game.turn
    assert restored.status == game.status
    assert restored.player1 == game.player1
    assert restored.player2 == game.player2