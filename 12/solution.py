"""
Solution to the twelfth challenge, identification of paths through
cave networks.

"""
from collections import defaultdict
from os import PathLike
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

ROOT = Path(__file__).absolute().parent


Name = str
"""The name of a cave."""

CavePath = List["Cave"]
"""A sequence of caves which lead through the network."""


class Cave:
    """A node within the cave network."""

    def __init__(self, name: Optional[Name] = None):
        self.name = name
        self._connections: List[Cave] = []

    @property
    def connections(self) -> Iterator["Cave"]:
        """An iterator over the caves that the cave is connected to."""
        yield from iter(self._connections)

    @property
    def is_small(self) -> bool:
        """A bool indicating whether the cave is small."""
        if self.name is None:
            raise ValueError("Unnamed cave can't be big or small!")
        return self.name == self.name.lower()

    def add_connection(self, other: "Cave"):
        """Add a connection from this cave to the other cave."""
        if not isinstance(other, Cave):
            raise ValueError("Can't make connection to non-cave.")
        if other not in self._connections:
            self._connections.append(other)
        if self not in other._connections:  # pylint: disable=protected-access
            other._connections.append(self)  # pylint: disable=protected-access


class CaveNetwork:  # pylint: disable=too-few-public-methods
    """A graph-like object representing the cave network."""

    def __init__(self, adjacency_list: Iterable[Tuple[Name, Name]]):
        self._nodes: Dict[Name, Cave] = defaultdict(Cave)
        for name_a, name_b in adjacency_list:
            self._nodes[name_a].add_connection(self._nodes[name_b])

        for name, node in self._nodes.items():
            node.name = name

    def _build_paths(
        self,
        current_node: Cave,
        allow_single_second_visit: bool = False,
        current_path: Optional[CavePath] = None,
    ) -> Iterator[CavePath]:
        """
        Iterate through a series of paths through the cave network from `current_node`
        to the end node.

        """

        path = current_path or [current_node]
        for cave in current_node.connections:
            if cave.name == "start":
                continue
            if cave.name == "end":
                yield [*path, cave]
                continue

            if cave.is_small and cave in path:
                if not allow_single_second_visit:
                    continue

                small_caves = filter(lambda cave: cave.is_small, path)
                if any(path.count(cave) == 2 for cave in small_caves):
                    continue

            yield from self._build_paths(cave, allow_single_second_visit, [*path, cave])

    def enumerate_paths(
        self, allow_single_second_visit: bool = False
    ) -> Iterator[CavePath]:
        """
        Iterate through the paths in the cave network from start to finish.

        By default, small caves will only be visited once. If
        `allow_single_second_visit` is set to `True`, a single small cave can be
        visited twice.

        """
        yield from self._build_paths(self._nodes["start"], allow_single_second_visit)


def parse_input(path: PathLike) -> CaveNetwork:
    """Parse a cave network from the input."""
    with open(path, "r", encoding="utf-8") as file:
        adjacency_list = []

        for row in map(str.rstrip, file):
            elem_a, elem_b = row.split("-")
            adjacency_list.append((elem_a, elem_b))

        return CaveNetwork(adjacency_list)


def main():
    """Check the number of paths through the cave system."""
    network = parse_input(ROOT.joinpath("data", "input_1.txt"))
    n_paths = sum(1 for _ in network.enumerate_paths())
    print(f"{n_paths} paths through the network.")

    n_paths_visit_small_twice = sum(1 for _ in network.enumerate_paths(True))
    print(
        f"{n_paths_visit_small_twice} paths through the network visiting a "
        + "single small cave twice."
    )


if __name__ == "__main__":
    main()
