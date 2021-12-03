"""
Solution to the third challenge, calculating the sub's power
usage and life support rating.

"""
from os import PathLike
from pathlib import Path
from typing import Sequence, List, Literal

ROOT = Path(__file__).absolute().parent

DiagnosticBit = int
DiagnosticArray = List[DiagnosticBit]
PositionBit = int
PositionSequence = Sequence[PositionBit]


def parse_diagnostic_input(path: PathLike) -> List[DiagnosticArray]:
    """
    Parse the list of measurements, returning a list of bits for each entry.

    """
    with open(path, "r") as file:
        return [list(map(int, row.rstrip())) for row in file if row]


def parse_power_input(path: PathLike) -> List[PositionSequence]:
    """
    Parse the list of measurements, returning a list of bits for each
    position. This is a transposed version of the diagnostic input.

    """
    return list(zip(*parse_diagnostic_input(path)))


def get_power_consumption(positions: Sequence[PositionSequence]) -> int:
    """
    Get the sub's power consumption by calculating the product of the
    gamma and epsilon rates.

    """
    most_common_bits = [round(sum(bits) / len(bits)) for bits in positions]
    least_common_bits = [int(not digit) for digit in most_common_bits]
    gamma_bitstring = "".join(map(str, most_common_bits))
    epsilon_bitstring = "".join(map(str, least_common_bits))

    return int(gamma_bitstring, 2) * int(epsilon_bitstring, 2)


def get_subsystem_rating(
    readings: Sequence[DiagnosticArray],
    subsystem: Literal["oxygen_generator", "co2_scrubber"],
    bit_index: int = 0,
) -> int:
    """Get the rating for a given life support subsystem."""
    if subsystem not in ("oxygen_generator", "co2_scrubber"):
        raise ValueError("Invalid subsystem")

    if len(readings) == 1:
        bitstring = "".join(map(str, readings[0]))
        return int(bitstring, 2)

    bits = [reading[bit_index] for reading in readings]
    average = sum(bits) / len(bits)
    keep_bit = 1 if average == 0.5 else round(average)
    if subsystem == "co2_scrubber":
        keep_bit = int(not keep_bit)

    to_keep = [readings[index] for index, bit in enumerate(bits) if bit == keep_bit]

    return get_subsystem_rating(to_keep, subsystem, bit_index + 1)


def get_life_support_rating(readings: Sequence[DiagnosticArray]):
    """Get the rating for the life support system."""
    oxygen_gen_rating = get_subsystem_rating(readings, "oxygen_generator")
    co2_scrubber_rating = get_subsystem_rating(readings, "co2_scrubber")
    return oxygen_gen_rating * co2_scrubber_rating


def main():
    """Read in the data and calculate distance travelled."""
    power_input = parse_power_input(ROOT.joinpath("data", "input_1.txt"))
    power_consumption = get_power_consumption(power_input)
    print(f"Calculated power to be {power_consumption} units.")

    diagnostic_input = parse_diagnostic_input(ROOT.joinpath("data", "input_1.txt"))
    life_support_rating = get_life_support_rating(diagnostic_input)
    print(f"Calculated life support rating to be {life_support_rating}.")


if __name__ == "__main__":
    main()
