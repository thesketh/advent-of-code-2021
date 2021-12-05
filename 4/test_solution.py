"""Tests using AOC-provided example data."""
from pathlib import Path

from solution import parse_input, get_winning_scores

ROOT = Path(__file__).absolute().parent


def test_first_score_calc():
    """Test that the first bingo score can be calculated correctly from test data."""
    boards, numbers = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    _, first_score = next(get_winning_scores(boards, numbers))
    assert first_score == 4512


def test_last_score_calc():
    """Test that the last bingo score can be calculated correctly from test data."""
    boards, numbers = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    *_, (_, last_score) = get_winning_scores(boards, numbers)
    assert last_score == 1924
