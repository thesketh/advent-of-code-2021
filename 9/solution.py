"""
Solution to the ninth challenge, calculating risk from hydrothermal
vents.

"""
from functools import reduce
from itertools import chain, tee
from operator import mul
from os import PathLike
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar

ROOT = Path(__file__).absolute().parent

IterType = TypeVar("IterType")

Position = Tuple[int, int]
"""The position within the height map, represented by X and Y coordinates."""

Height = int
"""The height of the hydrothermal vents. Lower heights are more dangerous."""

RiskLevel = int
"""An indication of the level of risk within a HeightMap."""

HeightMap = List[List[Height]]
"""A 2D scan of the surface of the cave."""

Basin = Set[Position]
"""A basin within the surface of the cave."""


def parse_input(path: PathLike) -> HeightMap:
    """Scan the input, returning a height map."""
    with open(path, "r", encoding="utf-8") as file:
        return list(map(lambda line: list(map(int, line.rstrip())), file))


def sandwich_iterator(
    iterable: Iterable[IterType],
) -> Iterator[Tuple[Optional[IterType], IterType, Optional[IterType]]]:
    """
    Iterate through an iterable, yielding a tuple containing the item before
    (or `None`) the item, and the item after (or `None`).

    """
    lagging: Iterator[Optional[IterType]]
    current: Iterator[IterType]
    leading: Iterator[Optional[IterType]]

    lagging, current, leading = tee(iterable, 3)
    lagging = chain([None], lagging)

    try:
        next(leading)
    except StopIteration:
        leading = iter([None])
    else:
        leading = chain(leading, [None])

    for tup in zip(lagging, current, leading):
        yield tup


def get_depressions(height_map: HeightMap) -> Dict[Position, Height]:
    """Calculate the depressions within a height map."""
    depressions = {}

    rows = sandwich_iterator(height_map)
    for row_index, (lag_row, row, lead_row) in enumerate(rows):
        for index, (lag, height, lead) in enumerate(sandwich_iterator(row)):
            if lag_row is not None and height >= lag_row[index]:
                continue
            if lag is not None and height >= lag:
                continue
            if lead is not None and height >= lead:
                continue
            if lead_row is not None and height >= lead_row[index]:
                continue

            depressions[row_index, index] = height

    return depressions


def calculate_risk_level_positional(depressions: Dict[Position, Height]) -> int:
    """
    Calculate the risk level of a height map based only on single
    positions.

    """
    return sum([height + 1 for height in depressions.values()])


def get_adjacent_positions(
    height_map: HeightMap, position: Position
) -> List[Tuple[Position, Height]]:
    """Get the positions adjacent to a particular point."""
    positions = []
    x_pos, y_pos = position

    for difference in (-1, 1):
        new_x = x_pos + difference
        if new_x >= 0:
            try:
                positions.append(((new_x, y_pos), height_map[new_x][y_pos]))
            except IndexError:
                pass

        new_y = y_pos + difference
        if new_y >= 0:
            try:
                positions.append(((x_pos, new_y), height_map[x_pos][new_y]))
            except IndexError:
                pass

    return positions


def get_basin(
    height_map: HeightMap,
    depression: Position,
    current_basin: Optional[Basin] = None,
) -> Basin:
    """Get a basin, given a height map and the point of the depression."""
    x_pos, y_pos = depression
    depression_height = height_map[x_pos][y_pos]
    basin = current_basin or set()
    basin.add(depression)

    for position, height in get_adjacent_positions(height_map, depression):
        if position in basin:
            continue

        if 9 > height >= depression_height:
            get_basin(height_map, position, basin)

    return basin


def calculate_risk_level_basins(height_map: HeightMap, depressions: Dict[Position, Height]) -> int:
    """
    Calculate the risk level of a height map based on the three
    largest basins.

    """
    basins = [get_basin(height_map, depression) for depression in depressions]
    basin_sizes = sorted(map(len, basins), reverse=True)
    return reduce(mul, basin_sizes[0:3], 1)


def main():
    """Scan the height map for danger."""
    height_map = parse_input(ROOT.joinpath("data", "input_1.txt"))
    depressions = get_depressions(height_map)

    risk_level = calculate_risk_level_positional(depressions)
    print(f"The risk level is {risk_level} based on single positions.")

    risk_level = calculate_risk_level_basins(height_map, depressions)
    print(f"The risk level is {risk_level} based on basins.")


if __name__ == "__main__":
    main()
