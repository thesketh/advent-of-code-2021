"""Tests using AOC-provided example data."""
from pathlib import Path

import pytest

from solution import parse_input

ROOT = Path(__file__).absolute().parent


@pytest.mark.parametrize(
    "test_file_name,num_paths",
    [("test_input_1.txt", 10), ("test_input_2.txt", 19), ("test_input_3.txt", 226)],
)
def test_path_counting(test_file_name: str, num_paths: int):
    """Test that paths can be counted from examples."""
    network = parse_input(ROOT.joinpath("data", test_file_name))
    assert sum(1 for _ in network.enumerate_paths()) == num_paths


@pytest.mark.parametrize(
    "test_file_name,num_paths",
    [("test_input_1.txt", 36), ("test_input_2.txt", 103), ("test_input_3.txt", 3509)],
)
def test_path_counting_twice_small(test_file_name: str, num_paths: int):
    """
    Test that paths can be counted from examples if we visit a single small
    cave twice.

    """
    network = parse_input(ROOT.joinpath("data", test_file_name))
    assert sum(1 for _ in network.enumerate_paths(True)) == num_paths
