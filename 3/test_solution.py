"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import (
    parse_diagnostic_input,
    parse_power_input,
    get_power_consumption,
    get_subsystem_rating,
    get_life_support_rating,
)

ROOT = Path(__file__).absolute().parent


def test_power_calc():
    """Test that the power can be calculated correctly from test data."""
    input_list = parse_power_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert get_power_consumption(input_list) == 198


def test_get_subsystem_rating():
    """Test that getting a life support subsystem's rating works."""
    input_list = parse_diagnostic_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert get_subsystem_rating(input_list, "oxygen_generator") == 23
    assert get_subsystem_rating(input_list, "co2_scrubber") == 10


def test_get_life_support_rating():
    """Test that getting the life support rating works."""
    input_list = parse_diagnostic_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert get_life_support_rating(input_list) == 230
