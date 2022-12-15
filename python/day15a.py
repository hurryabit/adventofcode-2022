from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 15
EXAMPLE_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
EXAMPLE_TARGET_Y = 10
EXAMPLE_OUTPUT = 26


def solve(reader: io.TextIOBase, targetY: int) -> int:
    beacons = set()
    covered = set()
    for line in reader.readlines():
        match = re.match(
            "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        [sX, sY, bX, bY] = [int(s) for s in match.groups()]
        if bY == targetY:
            beacons.add(bX)
        dist = abs(sX - bX) + abs(sY - bY)
        budget = dist - abs(sY - targetY)
        if budget >= 0:
            for x in range(sX - budget, sX + budget + 1):
                covered.add(x)
    return len(covered - beacons)


assert solve(io.StringIO(EXAMPLE_INPUT), EXAMPLE_TARGET_Y) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file, 2_000_000)
        print(f"{solution} positions cannot contain a beacon.")


if __name__ == "__main__":
    main()
