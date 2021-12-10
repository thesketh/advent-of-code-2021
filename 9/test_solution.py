"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import get_depressions, parse_input, calculate_risk_level_positional, calculate_risk_level_basins

ROOT = Path(__file__).absolute().parent


def test_calculate_risk_level_positional():
    """
    Test that the risk level can be calculated based on individual
    positions.

    """
    height_map = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    depressions = get_depressions(height_map)
    assert calculate_risk_level_positional(depressions) == 15


def test_calculate_risk_level_basins():
    """
    Test that the risk level can be calculated from basins.

    """
    height_map = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    depressions = get_depressions(height_map)
    assert calculate_risk_level_basins(height_map, depressions) == 1134
