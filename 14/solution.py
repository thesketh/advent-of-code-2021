"""
Solution to the fourteenth challenge, polymerisation.

"""
from itertools import tee
from collections import Counter
from os import PathLike
from pathlib import Path
from typing import Iterator, MutableMapping, Sequence, Tuple

ROOT = Path(__file__).absolute().parent


Element = str
"""A single character representing an element."""

ElementPair = Tuple[Element, Element]
"""A pair of elements which occur in sequence."""

Polymer = Sequence[Element]
"""A polymer. This is any sequence of elements."""

InsertionRules = MutableMapping[ElementPair, Element]
"""A mapping between a tuple of two elements and the element to insert between them."""


def parse_input(path: PathLike) -> Tuple[Polymer, InsertionRules]:
    """Parse a polymer and some insertion rules from the input."""
    with open(path, "r", encoding="utf-8") as file:
        lines = (line for line in map(str.rstrip, file) if line)
        return next(lines), {(line[0], line[1]): line[-1] for line in lines}


def polymerise(polymer: Polymer, rules: InsertionRules) -> Iterator[Counter[Element]]:
    """Polymerise the chain, yielding the element counts after each step."""
    element_counts = Counter(polymer)

    current, successor = tee(iter(polymer))
    try:
        next(successor)
    except StopIteration as err:
        raise ValueError("Initial polymer length must be at least 2") from err

    pairs: MutableMapping[ElementPair, int] = Counter(zip(current, successor))
    while True:
        matched_pairs = pairs.keys() & rules.keys()
        if not matched_pairs:
            return

        # For unmatched pairs of elements, do nothing.
        new_pairs = {pair: pairs[pair] for pair in pairs.keys() - rules.keys()}

        # For matched pairs, insert the new element and update the counts.
        for pair in matched_pairs:
            count = pairs[pair]
            new_element = rules[pair]

            first, last = pair
            for new_pair in ((first, new_element), (new_element, last)):
                new_pairs[new_pair] = new_pairs.get(new_pair, 0) + count
            element_counts[new_element] += count

        pairs = new_pairs
        yield element_counts


def main():
    """Perform elemental analysis of polymers after a number of steps."""
    polymer, insertion_rules = parse_input(ROOT.joinpath("data", "input_1.txt"))

    for step, element_counts in enumerate(polymerise(polymer, insertion_rules), 1):
        if step not in (10, 40):
            continue

        most_abundant, *_, least_abundant = element_counts.most_common()
        most_abundant_element, max_count = most_abundant
        least_abundant_element, min_count = least_abundant
        print(
            f"Difference in abundance between {most_abundant_element!r} and "
            + f"{least_abundant_element!r} is {max_count - min_count} after "
            + f"{step} steps"
        )

        if step == 40:
            break


if __name__ == "__main__":
    main()
