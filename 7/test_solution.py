"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, get_min_fuel_usage

ROOT = Path(__file__).absolute().parent


def test_get_min_fuel_usage_constant():
    """
    Test that the minimum fuel usage is calculated correctly with constant
    fuel burn.

    """
    crab_positions = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert get_min_fuel_usage(crab_positions, "constant") == 37


def test_get_min_fuel_usage_increasing():
    """
    Test that the minimum fuel usage is calculated correctly with increasing
    fuel burn.

    """
    crab_positions = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert get_min_fuel_usage(crab_positions, "increasing") == 168
