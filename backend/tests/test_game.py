import pytest

from app.game import Game


@pytest.fixture
def game():
    game = Game("TEST01")
    game.player1 = "player-1"
    game.player2 = "player-2"
    game.status = "playing"

    return game


def play(game, moves):
    for column in moves:
        game.make_move(column)


@pytest.mark.parametrize(
    "moves",
    [
        # Horizontal
        [0, 0, 1, 1, 2, 2, 3],

        # Vertical
        [0, 1, 0, 1, 0, 1, 0],

        # Diagonal
        [
            0, 1,
            1, 2,
            4, 2,
            2, 3,
            4, 3,
            5, 3,
            3,
        ],
    ],
)
def test_player_one_wins(
    game,
    moves,
):
    play(game, moves)

    assert game.winner == 1
    assert game.status == "finished"


def test_turn_switches(game):
    game.make_move(0)
    assert game.turn == 2

    game.make_move(1)
    assert game.turn == 1


def test_pieces_fall_and_stack(game):
    game.make_move(3)
    game.make_move(3)

    assert game.board[5][3] == 1
    assert game.board[4][3] == 2


def test_invalid_column(game):
    with pytest.raises(
        ValueError,
        match="Invalid column",
    ):
        game.make_move(10)


def test_full_column(game):
    play(
        game,
        [0, 0, 0, 0, 0, 0],
    )

    with pytest.raises(
        ValueError,
        match="Column is full",
    ):
        game.make_move(0)


def test_serialization(game):
    game.make_move(3)
    game.make_move(4)

    restored = Game.from_dict(
        game.to_dict()
    )

    assert restored.to_dict() == game.to_dict()