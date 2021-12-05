"""
Solution to the fourth challenge, beating the squid at bingo.

"""
from os import PathLike
from itertools import chain, islice
from pathlib import Path
from typing import FrozenSet, Iterator, Optional, Sequence, Set, Tuple

ROOT = Path(__file__).absolute().parent

Grid = Sequence[Sequence[int]]
"""A representation of a bingo board as a list of lists (rows) of integers."""
Row = FrozenSet[int]
"""A row in a bingo board."""
Column = FrozenSet[int]
"""A column in a bingo board."""
BoardScore = int
"""The bingo board's contribution to the final score."""
Score = int
"""The score of the board. A `BoardScore` multiplied by the last number called."""


class BingoBoard:
    """A bingo board, representing a grid of integers."""

    def __init__(self, grid: Grid):
        self._rows = [frozenset(row) for row in grid]
        self._columns = [frozenset(column) for column in zip(*grid)]

    @property
    def rows(self) -> Iterator[Row]:
        """An iterator over the rows in the board (as sets of ints)."""
        return iter(self._rows)

    @property
    def columns(self) -> Iterator[Column]:
        """An iterator over the columns in the board (as sets of ints)."""
        return iter(self._columns)

    def score(self, numbers: Set[int]) -> Optional[BoardScore]:
        """
        Return the board's component of the final bingo score. This should be
        multiplied by the last called number to obtain the final score.

        """
        for sequence in chain(self.rows, self.columns):
            if sequence < numbers:
                return sum({num for row in self.rows for num in row} - numbers)
        return None


def parse_input(path: PathLike) -> Tuple[Sequence[BingoBoard], Sequence[int]]:
    """
    Parse the bingo input, returning a sequence of `BingoBoard`s and a sequence
    of the numbers being called.

    """
    boards = []

    with open(path, "r") as file:
        numbers = list(map(int, next(file).rstrip().split(",")))
        next(file)

        while True:
            grid = []
            for row in iter(lambda: next(file).strip(), ""):
                grid.append([int(num) for num in row.split()])

            if not grid:
                break

            boards.append(BingoBoard(grid))

    return boards, numbers


def get_winning_scores(
    boards: Sequence[BingoBoard], number_sequence: Iterator[int]
) -> Iterator[Tuple[BingoBoard, Score]]:
    """
    Check a sequence of bingo boards, yielding the board and score in order of
    when the board won.

    """
    number_iterator = iter(number_sequence)
    number_set = set(islice(number_iterator, 5))
    winners = {}

    for number in number_iterator:
        number_set.add(number)

        for board in filter(lambda board: board not in winners, boards):
            board_score = board.score(number_set)
            if board_score is None:
                continue

            score = board_score * number
            winners[board] = score

            yield board, score

        if len(boards) == len(winners):
            return

    raise ValueError("No winning boards.")


def main():
    """Read in the data and output the first and last bingo scores."""
    boards, number_sequence = parse_input(ROOT.joinpath("data", "input_1.txt"))
    score_iterator = get_winning_scores(boards, number_sequence)

    first_board, first_score = next(score_iterator)
    first_board_index = boards.index(first_board) + 1
    print(f"First winning bingo score is {first_score} (board {first_board_index}).")

    try:
        *_, (last_board, last_score) = score_iterator
        last_board_index = boards.index(last_board) + 1
    except StopIteration:
        last_board, last_score = first_board, first_score
        last_board_index = first_board_index
    print(f"Last winning bingo score is {last_score} (board {last_board_index}).")


if __name__ == "__main__":
    main()
