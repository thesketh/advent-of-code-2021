"""
Solution to the sixth challenge, calculating the proliferation of
lanternfish.

"""
from collections import Counter
from os import PathLike
from pathlib import Path
from typing import Sequence, Iterable

ROOT = Path(__file__).absolute().parent


LanternFish = int
"""A lanternfish, represented by the number of days until spawn."""


def parse_input(path: PathLike) -> Sequence[LanternFish]:
    """Read in the sequence of lanternfish counts from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return list(map(int, next(file).rstrip().split(",")))


def count_lanternfish_after(lanternfish: Iterable[LanternFish], n_days: int) -> int:
    """Count the number of lanternfish after a given number of days."""
    fish_counter = Counter(lanternfish)

    for _ in range(n_days):
        n_spawned = fish_counter.pop(0, 0)

        for days_til_spawn in range(1, 9):
            fish_counter[days_til_spawn - 1] = fish_counter[days_til_spawn]

        fish_counter[6] += n_spawned
        fish_counter[8] = n_spawned

    return sum(fish_counter.values())


def main():
    """Perform the lanternfish population analysis."""
    all_lanternfish = parse_input(ROOT.joinpath("data", "input_1.txt"))

    n_lanternfish = count_lanternfish_after(all_lanternfish, n_days=80)
    print(f"{n_lanternfish} fish after 80 days.")

    n_lanternfish = count_lanternfish_after(all_lanternfish, n_days=256)
    print(f"{n_lanternfish} fish after 256 days.")


if __name__ == "__main__":
    main()
