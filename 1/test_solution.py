"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, count_increases_pairwise, count_increases_window


ROOT = Path(__file__).absolute().parent


def test_pairwise_count():
    """Test that the pairwise implementation works on the test data."""
    input_list = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert count_increases_pairwise(input_list) == 7


def test_window_count():
    """Test that the sliding window implementation works on the test data."""
    input_list = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert count_increases_window(input_list) == 5
