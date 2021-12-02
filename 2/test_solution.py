"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, calculate_distance


ROOT = Path(__file__).absolute().parent


def test_distance_calc():
    """Test that the distance can be calculated correctly from test data."""
    input_list = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert calculate_distance(input_list) == 150


def test_distance_calc_with_aim():
    """
    Test that the distance can be calculated correctly from test data using
    the movement method from the manual.

    """
    input_list = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert calculate_distance(input_list, read_manual=True) == 900
