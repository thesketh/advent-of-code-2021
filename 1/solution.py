"""
Solution to the first problem, calculating the number of times that the depth
increases.

"""
from collections import deque
from os import PathLike
from pathlib import Path
from typing import List, Iterator, Iterable, Sequence, Tuple, TypeVar

IterType = TypeVar("IterType")
ROOT = Path(__file__).absolute().parent


def parse_input(path: PathLike) -> List[int]:
    """Parse the list of depths from the file."""
    with open(path, "r") as file:
        return list(map(int, file))


def iterate_window(
    iterable: Iterable[IterType], size: int
) -> Iterator[Tuple[IterType, ...]]:
    """
    Iterate through an iterable, returning the item and the next
    `size - 1` items.

    """
    iterator = iter(iterable)
    try:
        items = deque(next(iterator) for _ in range(size - 1))
    except StopIteration:
        return

    for item in iterator:
        items.append(item)
        yield tuple(items)
        items.popleft()


def count_increases_pairwise(readings: Sequence[int]) -> int:
    """Count the number of times a reading increases."""
    counter = 0

    for previous_reading, current_reading in iterate_window(readings, 2):
        if current_reading > previous_reading:
            counter += 1

    return counter


def count_increases_window(readings: Sequence[int]) -> int:
    """Count the number of times the sum of a three-item window increases."""
    counter = 0

    for prev_window, curr_window in iterate_window(iterate_window(readings, 3), 2):
        if sum(curr_window) > sum(prev_window):
            counter += 1

    return counter


def main():
    """Read in the data and count the number of increases."""
    input_list = parse_input(ROOT.joinpath("data", "input_1.txt"))

    pairwise_increases = count_increases_pairwise(input_list)
    print(f"Depth increased {pairwise_increases} times pairwise.")
    window_increases = count_increases_window(input_list)
    print(f"Depth increased {window_increases} times in sliding window.")


if __name__ == "__main__":
    main()
