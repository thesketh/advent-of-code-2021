"""Tests using AOC-provided example data."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from textwrap import dedent

from solution import parse_input

ROOT = Path(__file__).absolute().parent


def test_num_marks_after_folds():
    """Test that the number of marks can be counted after a fold."""
    sheet, folds = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    assert sheet.count_marks() == 18
    new_sheet = sheet.fold(*folds[0])
    assert new_sheet.count_marks() == 17
    new_sheet = new_sheet.fold(*folds[1])
    assert new_sheet.count_marks() == 16


def test_display_after_folds():
    """Test that the actual display matches what's expected after folding."""
    sheet, folds = parse_input(ROOT.joinpath("data", "test_input_1.txt"))
    for fold in folds:
        sheet = sheet.fold(*fold)

    output = StringIO()
    with redirect_stdout(output):
        print(sheet, end="")
    output.seek(0)

    expected = dedent(
        """\
        █████
        █   █
        █   █
        █   █
        █████
        """
    )

    assert output.read() == expected
