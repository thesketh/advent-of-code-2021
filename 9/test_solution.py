"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, calculate_risk_level_positional

ROOT = Path(__file__).absolute().parent


def test_calculate_risk_level_positional():
    """
    Test that the risk level can be calculated.

    """
    height_map = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert calculate_risk_level_positional(height_map) == 15
