"""Tests using AOC-provided example data."""
from pathlib import Path

import pytest

from solution import parse_input, count_lanternfish_after

ROOT = Path(__file__).absolute().parent


@pytest.mark.parametrize("n_days,expected", [(18, 26), (80, 5934), (256, 26984457539)])
def test_num_lanternfish_after_n_days(n_days: int, expected: int):
    """
    Test that the number of lanternfish after a number of days can be
    successfully calculated from the test data.

    """
    all_lanternfish = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert count_lanternfish_after(all_lanternfish, n_days=n_days) == expected
