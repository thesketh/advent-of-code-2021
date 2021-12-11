"""
Solution to the eleventh challenge, navagation by flashing octopus.

"""
from itertools import count
from os import PathLike
from pathlib import Path
from typing import Iterator, List, Optional, Tuple

ROOT = Path(__file__).absolute().parent


OctopusGrid = List[List[int]]
"""A grid of octopus energy levels."""

Position = Tuple[int, int]
"""The position of an octopus in the grid."""


def parse_input(path: PathLike) -> OctopusGrid:
    """Parse a list of strings from the input."""
    with open(path, "r", encoding="utf-8") as file:
        return list(map(lambda string: list(map(int, string.rstrip())), file))


def flash_octopus(grid: OctopusGrid, position: Position) -> None:
    """
    Flash an octopus, increasing the energy level of the surrounding octopi
    by one.

    """
    for x_diff in range(-1, 2):
        for y_diff in range(-1, 2):
            if x_diff == y_diff == 0:
                continue

            x_pos = position[0] + x_diff
            y_pos = position[1] + y_diff
            if x_pos < 0 or y_pos < 0:
                continue

            try:
                value = grid[y_pos][x_pos]
            except IndexError:
                continue

            if value < 10:
                value += 1
                grid[y_pos][x_pos] = value
                if value == 10:
                    flash_octopus(grid, (x_pos, y_pos))


def iterate_flashes(grid: OctopusGrid, n_steps: Optional[int] = None) -> Iterator[int]:
    """
    Model the octopi's flashes, stepping through and yielding the number of
    flashes in each step. Where `n_steps` is provided, stop iterating after
    this many steps.

    """
    counter = 0
    while n_steps is None or counter < n_steps:
        for y_pos, row in enumerate(grid):
            for x_pos, value in enumerate(row):
                if value == 10:
                    continue

                value += 1
                grid[y_pos][x_pos] = value
                if value == 10:
                    flash_octopus(grid, (x_pos, y_pos))

        flashes = 0
        for y_pos, row in enumerate(grid):
            for x_pos, value in enumerate(row):
                if value == 10:
                    flashes += 1
                    grid[y_pos][x_pos] = 0

        yield flashes
        counter += 1


def main():
    """Count the octopus flashes."""
    grid = parse_input(ROOT.joinpath("data", "input_1.txt"))

    total_flashes, simultaneous = 0, False
    num_octopi = len(grid) * len(grid[0])
    for step_number, n_flashes in zip(count(1), iterate_flashes(grid)):
        total_flashes += n_flashes

        if step_number == 100:
            print(f"{total_flashes} flashes in 100 steps.")

        if n_flashes == num_octopi:
            print(f"First simultaneous flash at step {step_number}.")
            simultaneous = True

        if step_number > 100 and simultaneous:
            break

if __name__ == "__main__":
    main()
