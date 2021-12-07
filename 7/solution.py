"""
Solution to the seventh challenge, aligning crab submarines.

"""
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Callable, List, Literal

ROOT = Path(__file__).absolute().parent


Position = int
"""The position of a crab sub."""

FuelCost = int
"""The cost, in units of fuel, of a move."""


def parse_input(path: PathLike) -> List[Position]:
    """Return a sequence of horizontal positions of the crab subs."""
    with open(path, "r", encoding="utf-8") as file:
        return list(map(int, next(file).rstrip().split(",")))


def get_fuel_usage(
    crab_positions: List[Position],
    proposed_position: Position,
    fuel_cost_func: Callable[[Position, Position], FuelCost],
) -> FuelCost:
    """Get the fuel usage if all the crabs move to a specific position."""
    return sum([fuel_cost_func(pos, proposed_position) for pos in crab_positions])


def get_min_fuel_usage(
    crab_positions: List[Position],
    fuel_burn: Literal["constant", "increasing"] = "constant",
) -> FuelCost:
    """Get the fuel usage of the crabs if they align on the best position."""
    crab_positions = sorted(crab_positions)

    if fuel_burn == "constant":
        calc_fuel_usage = partial(
            get_fuel_usage, fuel_cost_func=lambda pos, proposed: abs(pos - proposed)
        )
        # Start at median position, fewest moves is best.
        test_position = crab_positions[len(crab_positions) // 2]

    elif fuel_burn == "increasing":
        calc_fuel_usage = partial(
            get_fuel_usage,
            fuel_cost_func=lambda pos, proposed: sum(range(1, abs(pos - proposed) + 1)),
        )
        # Start at mean position, shortest moves is best.
        test_position = round(sum(crab_positions) // len(crab_positions))

    else:
        raise ValueError("`fuel_burn` must be one of `{'constant', 'increasing'}`")

    fuel_usage = calc_fuel_usage(crab_positions, test_position)
    tested_positions = {
        test_position,
    }
    while True:
        for new_position in (test_position + 1, test_position - 1):
            if new_position in tested_positions:
                continue

            new_usage = calc_fuel_usage(crab_positions, new_position)
            if new_usage < fuel_usage:
                fuel_usage = new_usage
                tested_positions.add(new_position)
                test_position = new_position
                break
        else:
            return fuel_usage


def main():
    """Calculate the minimum crab fuel usage."""
    crab_positions = parse_input(ROOT.joinpath("data", "input_1.txt"))

    min_usage = get_min_fuel_usage(crab_positions)
    print(f"Minimum crab fuel use (with constant burn) is {min_usage} units.")

    min_usage = get_min_fuel_usage(crab_positions, "increasing")
    print(f"Minimum crab fuel use (with increasing burn) is {min_usage} units.")


if __name__ == "__main__":
    main()
