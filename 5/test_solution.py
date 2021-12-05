"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, calculate_line_overlap

ROOT = Path(__file__).absolute().parent


def test_aligned_line_overlap_calc():
    """
    Test that the number of overlaps can be calculated correctly from test data,
    including only lines which are X-aligned or Y-aligned.

    """
    lines = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert calculate_line_overlap(lines) == 5


def test_line_overlap_calc():
    """
    Test that the number of overlaps can be calculated correctly from test data.

    """
    lines = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert calculate_line_overlap(lines, aligned_only=False) == 12
