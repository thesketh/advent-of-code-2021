"""Tests using AOC-provided example data."""
from pathlib import Path
from typing import Mapping

import pytest

from solution import parse_input, polymerise

ROOT = Path(__file__).absolute().parent


@pytest.mark.parametrize(
    "num_steps,expected_length",
    [(1, 7), (5, 97), (10, 3073)],
)
def test_polymerisation(num_steps: int, expected_length: int):
    """Test that polymerisation produces sequences of the expected length."""
    polymer, insertion_rules = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    for step, counts in enumerate(polymerise(polymer, insertion_rules), 1):
        if step == num_steps:
            assert sum(counts.values()) == expected_length
            break


@pytest.mark.parametrize(
    "num_steps,expected_counts",
    [
        (1, {"N": 2, "C": 2, "B": 2, "H": 1}),
        (2, {"B": 6, "C": 4, "N": 2, "H": 1}),
        (3, {"B": 11, "N": 5, "C": 5, "H": 4}),
        (4, {"B": 23, "N": 11, "C": 10, "H": 5}),
    ],
)
def test_polymerisation_sequences(num_steps: int, expected_counts: Mapping[str, int]):
    """Test that polymerisation produces the expected elements."""
    polymer, insertion_rules = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    for step, counts in enumerate(polymerise(polymer, insertion_rules), 1):
        if step == num_steps:
            assert counts == expected_counts
            break
