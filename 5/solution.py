"""
Solution to the fifth challenge, calculating dangerous points where there
are overlapping lines of hydrothermal vents.

"""
from collections import Counter
from dataclasses import dataclass
from itertools import repeat
from os import PathLike
from pathlib import Path
from typing import Iterable, Iterator, MutableMapping, Sequence, Tuple

ROOT = Path(__file__).absolute().parent


Point = Tuple[int, int]


@dataclass(frozen=True)
class Line:
    """A representation of a line in, with a start and end."""

    start: Point
    end: Point

    def __post_init__(self):
        if len(self.start) != 2 or len(self.end) != 2:
            raise TypeError(f"`start` or `end` not a two-tuple: {self!r}")

    @property
    def is_along_axis(self) -> bool:
        """Whether the line is aligned with the X or Y axes."""
        return (self.start[0] == self.end[0]) or (self.start[1] == self.end[1])

    @property
    def points(self) -> Iterator[Point]:
        """An iterator of points in the line."""
        (start_x, start_y), (end_x, end_y) = self.start, self.end

        if start_x == end_x:
            x_vals: Iterable[int] = repeat(start_x)
        else:
            step = 1 if start_x < end_x else -1
            x_vals = range(start_x, end_x + step, step)

        if start_y == end_y:
            y_vals: Iterable[int] = repeat(start_y)
        else:
            step = 1 if start_y < end_y else -1
            y_vals = range(start_y, end_y + step, step)

        return zip(x_vals, y_vals)

    @classmethod
    def from_entry(cls, entry: str) -> "Line":
        """
        Parse a line from an entry. Entries take the following form:
        `"start_x,start_y -> end_x,end_y"` where `start_x`, `start_y`,
        `end_x` and `end_y` are all positive integers.

        >>> Line.from_entry("989,854 -> 521,854")
        Line(start=(989, 854), end=(521, 854))

        """
        positions = map(lambda string: string.split(","), entry.rstrip().split(" -> "))
        start, end = map(lambda position: tuple(map(int, position)), positions)
        return cls(start, end)  # type: ignore


def parse_input(path: PathLike) -> Sequence[Line]:
    """
    Parse the hydrothermal vent data, returning a sequence of `Line`s.

    """
    with open(path, "r", encoding="utf-8") as file:
        return list(map(Line.from_entry, file))


def calculate_line_overlap(lines: Iterable[Line], aligned_only: bool = True) -> int:
    """
    Calculate the number of overlapping lines. If `aligned_only` is True, consider
    only lines which are aligned to the X or Y axes.

    """
    point_counter: MutableMapping[Point, int] = Counter()

    for line in lines:
        if aligned_only and not line.is_along_axis:
            continue

        for point in line.points:
            point_counter[point] += 1

    n_overlapping = 0
    for count in point_counter.values():
        if count > 1:
            n_overlapping += 1

    return n_overlapping


def main():
    """Read in the data and calculate the number of dangerous positions."""
    lines = parse_input(ROOT.joinpath("data", "input_1.txt"))

    n_aligned_overlaps = calculate_line_overlap(lines)
    print(f"{n_aligned_overlaps} overlapping line(s) of X/Y aligned vents.")

    n_overlaps = calculate_line_overlap(lines, aligned_only=False)
    print(f"{n_overlaps} overlapping line(s) of vents.")


if __name__ == "__main__":
    main()
