import builtins
from typing import List

import simple_game


def run_scripted_game(moves: List[str]):
    game = simple_game.Game(rows=4, cols=4, seed=1)
    for move in moves:
        game.step(move)
    return game


def test_player_stays_within_bounds():
    game = simple_game.Game(rows=3, cols=3, seed=0)
    for _ in range(5):
        game.step("w")
    # player should stay on top row, center column
    assert game.player_pos == (0, 1)


def test_collision_triggers_game_over():
    game = simple_game.Game(rows=3, cols=3, seed=0)
    # force obstacle drop in same column by seeding
    game.step("")  # spawn one obstacle
    game.obstacles = [(game.rows - 2, game.cols // 2)]
    result = game.step("")
    assert result == "game-over"
    assert game.game_over is True


def test_scripted_moves_progress_score():
    moves = ["a", "d", ""]
    game = run_scripted_game(moves)
    assert game.score >= len(moves)


def test_render_shows_player_and_obstacles(monkeypatch):
    game = simple_game.Game(rows=2, cols=2, seed=0)
    game.obstacles = [(0, 0)]
    render = game.render()
    assert "X" in render
    assert "P" in render


def test_interactive_play_consumes_scripted_moves(monkeypatch, capsys):
    moves = iter(["a", "s", ""])

    def fake_input(prompt=""):
        return next(moves)

    monkeypatch.setattr(builtins, "input", fake_input)
    game = simple_game.Game(rows=3, cols=3, seed=2)
    simple_game.interactive_play(game, moves=["w", "a"], max_turns=2)
    captured = capsys.readouterr().out
    assert "[auto] w" in captured
    assert "Score" in captured

