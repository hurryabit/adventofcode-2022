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
EXAMPLE_LIMIT = 20
EXAMPLE_OUTPUT = 56000011


def freq(x: int, y: int) -> int:
    return 4_000_000 * x + y


def solve(reader: io.TextIOBase, limit: int) -> int:
    covered = [[] for _ in range(0, limit + 1)]
    for line in reader.readlines():
        match = re.match(
            "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        [sX, sY, bX, bY] = [int(s) for s in match.groups()]
        dist = abs(sX - bX) + abs(sY - bY)

        for y in range(max(0, sY - dist), min(limit, sY + dist) + 1):
            budget = dist - abs(sY - y)
            covered[y].append((sX - budget, sX + budget))

    for (y, intervals) in enumerate(covered):
        intervals.sort()
        wantedX = 0
        for (left, right) in intervals:
            if left > wantedX:
                return freq(wantedX, y)
            if right >= wantedX:
                wantedX = right + 1
            if wantedX > limit:
                break
        if wantedX <= limit:
            return freq(wantedX, y)


assert solve(io.StringIO(EXAMPLE_INPUT), EXAMPLE_LIMIT) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file, 4_000_000)
        print(f"The tuning frequency is {solution}.")


if __name__ == "__main__":
    main()
