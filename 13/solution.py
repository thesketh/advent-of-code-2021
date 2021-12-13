"""
Solution to the thirteenth challenge, entering a code for the thermal
camera.

"""
import re
from os import PathLike
from pathlib import Path
from typing import Collection, List, Tuple

ROOT = Path(__file__).absolute().parent


Coordinate = Tuple[int, int]
"""A 2-D coordinate, representing a mark on the paper."""


Fold = Tuple[str, int]
"""
A representation of a fold. This contains a dimension (one of `{'x', 'y'}`)
and the position to fold along on that axis.

"""


class Sheet:
    """
    A transparent sheet, containing marks which can be seen even after
    folding.

    """

    def __init__(self, marks: Collection[Coordinate]):
        self._marks = marks

    def __str__(self) -> str:
        max_x = max(mark[0] for mark in self._marks)
        max_y = max(mark[1] for mark in self._marks)

        rows = []
        for y_index in range(max_y + 1):
            row = []
            for x_index in range(max_x + 1):
                # \u2588 is Unicode full block.
                row.append("\u2588" if (x_index, y_index) in self._marks else " ")
            rows.append("".join(row))
        rows.append("")
        return "\n".join(rows)

    def fold(self, fold_dimension: str, position: int) -> "Sheet":
        """Fold the sheet, returning a new sheet."""
        if fold_dimension not in ("x", "y"):
            raise ValueError("Dimension must be one of {'x', 'y'}")

        index = 0 if fold_dimension == "x" else 1
        new_marks = set()

        for mark in self._marks:
            if mark[index] == position:
                continue
            if mark[index] < position:
                new_marks.add(mark)
                continue

            if index == 0:
                mark = (2 * position - mark[0], mark[1])
            else:
                mark = (mark[0], 2 * position - mark[1])
            new_marks.add(mark)

        return self.__class__(new_marks)

    def count_marks(self) -> int:
        """Return the number of marks on the paper."""
        return len(set(self._marks))


def parse_input(path: PathLike) -> Tuple[Sheet, List[Fold]]:
    """Parse a transparent code sheet from the input."""
    with open(path, "r", encoding="utf-8") as file:
        str_positions = map(lambda line: line.split(","), iter(file.__next__, "\n"))
        mark_positions = {(int(line[0]), int(line[1])) for line in str_positions}

        sheet = Sheet(mark_positions)

        folds = []
        patt = re.compile("^fold along ([xy])=([0-9]+)")
        for line in file:
            match = patt.match(line)
            if match:
                folds.append((match.group(1), int(match.group(2))))

        return sheet, folds


def main():
    """Count the number of marks after folding, then print the code."""
    sheet, folds = parse_input(ROOT.joinpath("data", "input_1.txt"))

    for fold_index, fold in enumerate(folds):
        sheet = sheet.fold(*fold)
        if fold_index == 0:
            n_marks = sheet.count_marks()
            print(f"{n_marks} marks after first fold.")

    print("\nThe code is:")
    print(sheet)


if __name__ == "__main__":
    main()
