import argparse
import random
from typing import List, Tuple


class Game:
    """
    A tiny dodge-the-blocks terminal game. The player ("P") moves on a grid while
    obstacles ("X") fall from the top. If an obstacle hits the player, the game ends.
    """

    MOVE_MAP = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
        "": (0, 0),  # allow empty input to stay in place
    }

    def __init__(self, rows: int = 6, cols: int = 6, seed: int | None = None):
        self.rows = rows
        self.cols = cols
        self.random = random.Random(seed)
        self.reset()

    def reset(self) -> None:
        self.turn = 0
        self.player_pos = (self.rows - 1, self.cols // 2)
        self.obstacles: List[Tuple[int, int]] = []
        self.game_over = False
        self.score = 0

    def spawn_obstacle(self) -> None:
        column = self.random.randrange(self.cols)
        self.obstacles.append((0, column))

    def move_player(self, direction: str) -> None:
        if direction not in self.MOVE_MAP:
            return
        dr, dc = self.MOVE_MAP[direction]
        r, c = self.player_pos
        nr, nc = max(0, min(self.rows - 1, r + dr)), max(0, min(self.cols - 1, c + dc))
        self.player_pos = (nr, nc)

    def advance_obstacles(self) -> None:
        self.obstacles = [(r + 1, c) for r, c in self.obstacles if r + 1 < self.rows]

    def check_collision(self) -> bool:
        return self.player_pos in self.obstacles

    def step(self, direction: str) -> str:
        if self.game_over:
            return "game-over"

        self.move_player(direction.lower())
        self.advance_obstacles()
        self.spawn_obstacle()
        self.turn += 1

        if self.check_collision():
            self.game_over = True
            return "game-over"

        self.score += 1
        return "continue"

    def render(self) -> str:
        grid = [["."] * self.cols for _ in range(self.rows)]
        for r, c in self.obstacles:
            grid[r][c] = "X"
        pr, pc = self.player_pos
        grid[pr][pc] = "P"
        return "\n".join(" ".join(row) for row in grid)


INTRO = """Dodge the Blocks
====================
Move with WASD (press Enter to wait). Avoid falling X blocks.
Score +1 each safe turn. Survive as long as possible!
"""


def interactive_play(game: Game, moves: List[str] | None, max_turns: int | None) -> None:
    print(INTRO)
    turn_limit = max_turns or float("inf")
    move_iter = iter(moves) if moves else None

    while game.turn < turn_limit and not game.game_over:
        print(f"\nTurn {game.turn + 1} | Score: {game.score}")
        print(game.render())

        if move_iter:
            try:
                raw_move = next(move_iter)
                print(f"[auto] {raw_move}")
            except StopIteration:
                move_iter = None
                raw_move = input("Move (w/a/s/d or Enter to wait): ")
        else:
            raw_move = input("Move (w/a/s/d or Enter to wait): ")

        state = game.step(raw_move.strip())
        if state == "game-over":
            print("\nYou got hit! Final board:")
            print(game.render())
            break

    print(f"\nGame finished after {game.turn} turns with score {game.score}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play a tiny dodge-the-blocks game")
    parser.add_argument("--rows", type=int, default=6, help="Grid rows (default: 6)")
    parser.add_argument("--cols", type=int, default=6, help="Grid columns (default: 6)")
    parser.add_argument("--moves", type=str, help="Comma-separated scripted moves, e.g. 'a,s,d'", default=None)
    parser.add_argument("--seed", type=int, help="Random seed for reproducible obstacle drops")
    parser.add_argument("--max-turns", type=int, help="Stop after this many turns even if alive")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scripted_moves = args.moves.split(",") if args.moves else None
    game = Game(rows=args.rows, cols=args.cols, seed=args.seed)
    interactive_play(game, scripted_moves, args.max_turns)


if __name__ == "__main__":
    main()
