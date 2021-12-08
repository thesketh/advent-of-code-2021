"""
Solution to the eighth challenge, parsing mangled seven segment
displays.

"""
from os import PathLike
from pathlib import Path
from typing import List, MutableMapping, Set, Tuple

ROOT = Path(__file__).absolute().parent


Segment = str
"""
A character representing a single segment in a seven-segment display.
This is a lowercase letter from 'a' to 'g' (inclusive). The canonical
representation of these is as follows:

```
 aaaa
b    c
b    c
 dddd
e    f
e    f
 gggg
```

"""


SegmentString = str
"""
A string representing the illuminated segments in a seven-segment display.
This will contain only one character per illuminated segment.

"""

InputSignals = List[SegmentString]
"""
A list of strings representing the 10 possible digits, in any order.
These need to be unscrambled to work out the mapping from these signals to
integers.

"""

DisplayDigits = List[SegmentString]
"""
A list of strings representing display values. After decoding the input
signals, the mapping should be applied to these to convert them to integers.

"""


class Display:  # pylint: disable=too-few-public-methods
    """
    A seven segment display. This is created from a list of 10 input
    signals (`SegmentString`s) which represent a digit.

    """

    def __init__(self, input_signals: InputSignals):
        digit_sets: List[Set[Segment]] = list(map(set, input_signals))  # type: ignore

        mapping: MutableMapping[int, Set[SegmentString]] = {}
        segments: MutableMapping[Segment, Segment] = {}

        input_lengths = {len(digit_set): digit_set for digit_set in digit_sets}
        mapping[1] = input_lengths[2]
        mapping[4] = input_lengths[4]
        mapping[7] = input_lengths[3]
        mapping[8] = input_lengths[7]
        for digit_set in mapping.values():
            digit_sets.remove(digit_set)

        proto_nine = mapping[4] | mapping[7]
        mapping[9] = self._get_digit_from_proto(digit_sets, proto_nine)
        segments["g"] = next(iter(mapping[9] - proto_nine))
        segments["e"] = next(iter(mapping[8] - mapping[9]))
        digit_sets.remove(mapping[9])

        proto_three = {*mapping[7], segments["g"]}
        mapping[3] = self._get_digit_from_proto(digit_sets, proto_three)
        segments["d"] = next(iter(mapping[3] - proto_three))
        digit_sets.remove(mapping[3])

        mapping[0] = mapping[8] - set(segments["d"])
        digit_sets.remove(mapping[0])

        mapping[6] = next(filter(lambda digit: len(digit) == 6, digit_sets))
        digit_sets.remove(mapping[6])

        mapping[5] = mapping[6] - set(segments["e"])
        digit_sets.remove(mapping[5])

        mapping[2] = next(iter(digit_sets))

        self._mapping = {frozenset(digit): value for value, digit in mapping.items()}

    def render(self, display_digits: List[SegmentString]) -> int:
        """Render a display value, returning it as an integer."""

        values = [str(self._mapping[frozenset(digit)]) for digit in display_digits]
        return int("".join(values))

    @staticmethod
    def count_unambiguos(display_digits: List[SegmentString]) -> int:
        """
        Count the unambiguous characters in the display (those which can be
        identified from length alone).

        """
        return sum([int(len(digit) in (2, 3, 4, 7)) for digit in display_digits])

    @staticmethod
    def _get_digit_from_proto(
        digits: List[Set[str]], proto_digit: Set[str]
    ) -> Set[str]:
        """
        Get a digit from a set of possibilities and a proto digit (the digit,
        minus) one segment.

        This assumes that there is only one possibility for the given scaffold.

        """
        expected_len = len(proto_digit) + 1
        contenders = filter(lambda digit: len(digit) == expected_len, digits)
        matched = filter(lambda digit: len(digit - proto_digit) == 1, contenders)

        try:
            return next(matched)
        except StopIteration as err:
            raise ValueError(f"Proto digit {proto_digit} not in {digits}") from err


def parse_input(path: PathLike) -> List[Tuple[Display, DisplayDigits]]:
    """
    Return a sequence of tuples containing a `Display` and the digits to
    be shown.
    """
    with open(path, "r", encoding="utf-8") as file:
        entries = map(lambda line: line.rstrip().split(" | "), file)

        data = []
        for input_signal_str, display_digit_str in entries:
            input_signals = input_signal_str.split()
            display_digits = display_digit_str.split()

            display = Display(input_signals)
            data.append((display, display_digits))

        return data


def main():
    """
    Count the number of 1s, 4s, 7s, and 8s in the output, and sum the
    output values.
    
    """
    input_data = parse_input(ROOT.joinpath("data", "input_1.txt"))

    total, count_simple = 0, 0
    for display, display_digits in input_data:
        count_simple += display.count_unambiguos(display_digits)
        total += display.render(display_digits)

    print(f"1, 4, 7 and 8 occur {count_simple} times in output.")
    print(f"The sum of the output values is {total}.")


if __name__ == "__main__":
    main()
