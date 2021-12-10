"""
Solution to the tenth challenge, fixing syntax errors.

"""
from collections import deque
from os import PathLike
from pathlib import Path
from typing import Deque, Iterable, List, Optional, Tuple

ROOT = Path(__file__).absolute().parent


BRACKETS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
"""A mapping from open bracket to close bracket."""

OPEN_BRACKETS = set(BRACKETS.keys())
"""The set of open brackets."""

CLOSE_BRACKETS = set(BRACKETS.values())
"""The set of close brackets."""

BRACKET_SYNTAX_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
"""The syntax score for each mismatched bracket."""

BRACKET_COMPLETION_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
"""The amount added to the completion score for each bracket."""


Completion = str
"""The combination of close bracket characters required to complete a string."""

Mismatch = str
"""The first mismatched close bracket in a string."""


def parse_input(path: PathLike) -> List[str]:
    """Return a sequence of brackets."""
    with open(path, "r", encoding="utf-8") as file:
        return list(map(str.rstrip, file))


def identify_bracket_errors(
    string: str,
) -> Tuple[Optional[Mismatch], Optional[Completion]]:
    """Identify the first mismatched bracket from a string."""
    brackets: Deque[str] = deque()

    for char in string:
        if char in OPEN_BRACKETS:
            brackets.append(char)
        elif not brackets:
            return char, None
        else:
            expected = BRACKETS[brackets.pop()]
            if char != expected and char in CLOSE_BRACKETS:
                return char, None

    brackets.reverse()
    return None, "".join(map(BRACKETS.__getitem__, brackets))


def score_mismatches(mismatches: Iterable[Mismatch]) -> int:
    """
    Score a collection of mismatched brackets, according to the rules for
    syntax checkers.

    """
    return sum(map(BRACKET_SYNTAX_SCORES.__getitem__, mismatches))


def score_completions(completions: Iterable[Completion]) -> int:
    """
    Score a list of completions, according to the rules for auto-formatters.

    """
    scores = []
    for completion in completions:
        score = 0
        for bracket in completion:
            score *= 5
            score += BRACKET_COMPLETION_SCORES[bracket]
        scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]


def main():
    """Parse the erroneous brackets."""
    strings = parse_input(ROOT.joinpath("data", "input_1.txt"))
    mismatches, completions = zip(*map(identify_bracket_errors, strings))

    syntax_score = score_mismatches(filter(None, mismatches))
    print(f"Syntax error score is {syntax_score}.")

    completion_score = score_completions(filter(None, completions))
    print(f"Completion score is {completion_score}.")


if __name__ == "__main__":
    main()
