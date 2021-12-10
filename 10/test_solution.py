"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import (
    parse_input,
    identify_bracket_errors,
    score_mismatches,
    score_completions,
)

ROOT = Path(__file__).absolute().parent


def test_identify_bracket_errors():
    """Test that the right bracket is flagged as erroneous."""
    strings = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    errors = map(identify_bracket_errors, strings)
    mismatches = [error[0] for error in errors if error[0] is not None]
    assert mismatches == ["}", ")", "]", ")", ">"]


def test_score_bracket_errors():
    """Test that the right bracket score is calculated."""
    strings = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    errors = map(identify_bracket_errors, strings)
    mismatches = [error[0] for error in errors if error[0] is not None]
    assert score_mismatches(mismatches) == 26397


def test_identify_completions():
    """Test that the right completions are identified."""
    strings = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    errors = map(identify_bracket_errors, strings)
    completions = [error[1] for error in errors if error[1] is not None]
    assert completions == ["}}]])})]", ")}>]})", "}}>}>))))", "]]}}]}]}>", "])}>"]


def test_score_completions():
    """Test that the correct score for the completions is identified."""
    strings = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    errors = map(identify_bracket_errors, strings)
    completions = [error[1] for error in errors if error[1] is not None]
    assert score_completions(completions) == 288957
