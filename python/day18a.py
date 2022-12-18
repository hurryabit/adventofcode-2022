from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 18
EXAMPLE_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
EXAMPLE_OUTPUT = 64


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: Point) -> Point:
        return Point(
            x=self.x+other.x,
            y=self.y+other.y,
            z=self.z+other.z,
        )


DIRECTIONS = [
    Point(-1, 0, 0),
    Point(1, 0, 0),
    Point(0, -1, 0),
    Point(0, 1, 0),
    Point(0, 0, -1),
    Point(0, 0, 1),
]


def solve(reader: io.TextIOBase) -> int:
    lava = set[Point]()
    for line in reader.readlines():
        [x, y, z] = line.strip().split(",")
        point = Point(x=int(x), y=int(y), z=int(z))
        lava.add(point)

    count = 0
    for point in lava:
        for dir in DIRECTIONS:
            if point + dir not in lava:
                count += 1

    return count


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The surface area is {solution}.")


if __name__ == "__main__":
    main()
