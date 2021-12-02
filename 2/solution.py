"""
Solution to the second problem, calculating distance travelled by the sub.

"""
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Iterable, List, Tuple

ROOT = Path(__file__).absolute().parent


AimChange = int
DepthChange = int
DistanceChange = int


@dataclass
class Movement:
    """A change in position of the sub."""

    direction: str
    """The direction of travel."""
    distance: int
    """The distance travelled in that direction."""

    def get_position_change(self) -> Tuple[DepthChange, DistanceChange]:
        """Get the change in position from the movement."""
        if self.direction == "up":
            return (-self.distance, 0)
        if self.direction == "down":
            return (self.distance, 0)
        if self.direction == "forward":
            return (0, self.distance)
        raise ValueError(f"Invalid direction {self.direction}")

    def get_aimed_position_change(
        self, aim: int
    ) -> Tuple[DepthChange, DistanceChange, AimChange]:
        """Get the change in position given the aim."""
        alignment_change, distance = self.get_position_change()
        if alignment_change:
            return (0, 0, alignment_change)
        return (distance * aim, distance, 0)


@dataclass
class Submarine:
    """A representation of the sub's position."""

    depth: int = 0
    """The depth of the sub."""
    distance: int = 0
    """The horizontal displacement of the sub."""
    aim: int = 0
    """The aim of the sub."""
    use_aim: bool = False
    """If `True`, calculate the sub's depth changes based on aim."""

    def move(self, movement: Movement):
        """Move the sub."""
        if self.use_aim:
            depth, distance, aim = movement.get_aimed_position_change(self.aim)
            self.aim += aim
        else:
            depth, distance = movement.get_position_change()

        self.depth += depth
        self.distance += distance

    @property
    def total_displacement(self) -> int:
        """The total distance travelled by the sub."""
        return self.depth * self.distance


def parse_input(path: PathLike) -> List[Movement]:
    """Parse the list of directions and distances."""
    with open(path, "r") as file:
        operations = []
        for line in file:
            direction, distance_str = line.split()
            operations.append(Movement(direction, int(distance_str)))

        return operations


def calculate_distance(movements: Iterable[Movement], read_manual: bool = False) -> int:
    """
    Calculate displacement of the sub from a series of movements.

    `read_manual` indicates whether you have read the sub's manual.

    """
    submarine = Submarine(use_aim=read_manual)

    for movement in movements:
        submarine.move(movement)

    return submarine.total_displacement


def main():
    """Read in the data and calculate distance travelled."""
    input_list = parse_input(ROOT.joinpath("data", "input_1.txt"))

    distance = calculate_distance(input_list)
    print(f"Calculated distance travelled to be {distance} units.")
    distance = calculate_distance(input_list, read_manual=True)
    print(f"Calculated distance travelled to be {distance} units after reading manual")


if __name__ == "__main__":
    main()
