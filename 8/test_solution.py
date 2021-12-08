"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, Display

ROOT = Path(__file__).absolute().parent


def test_count_unambiguous_output_digits():
    """
    Test that the number of unambiguous output digits can be counted as expected.
    
    """
    input_data = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    count_simple = 0
    for display, display_digits in input_data:
        count_simple += display.count_unambiguous(display_digits)

    assert count_simple == 26


def test_sum_outputs():
    """Test that the sum of the outputs can be counted as expected."""
    input_data = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    total = 0
    for display, display_digits in input_data:
        total += display.render(display_digits)

    assert total == 61229