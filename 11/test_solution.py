"""Tests using AOC-provided example data."""
# pylint: disable=redefined-outer-name
from itertools import count
from pathlib import Path
from typing import Iterator

import pytest

from solution import OctopusGrid, parse_input, iterate_flashes

ROOT = Path(__file__).absolute().parent


@pytest.fixture
def grid() -> Iterator[OctopusGrid]:
    """The test octopus grid."""
    yield parse_input(ROOT.joinpath("data", "test_input_1.txt"))


@pytest.mark.parametrize("n_steps,expected", [(10, 204), (100, 1656)])
def test_flash_counting(grid: OctopusGrid, n_steps: int, expected: int):
    """Test that `iterate_flashes` works as expected."""
    assert sum(iterate_flashes(grid, n_steps)) == expected


def test_first_simultaneous_flash(grid: OctopusGrid):
    """Test that octopi flash simultaneously at the expected time."""
    num_octopi = len(grid) * len(grid[0])

    for step_number, n_flashes in zip(count(1), iterate_flashes(grid)):
        if n_flashes == num_octopi:
            break

    assert step_number == 195  # pylint: disable=undefined-loop-variable
