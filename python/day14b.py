from __future__ import annotations
from collections.abc import Callable, Iterable
from typing import TypeVar
import io

DAY = 14
EXAMPLE_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
EXAMPLE_OUTPUT = 93


def parsePoint(s: str) -> tuple[int, int]:
    [x, y] = s.split(",")
    return (int(x), int(y))


def inclRange(a: int, b: int) -> Iterable[int]:
    return range(a, b + 1) if a <= b else range(b, a + 1)


A = TypeVar("A")


def findWith(xs: Iterable[A], p: Callable[[A], bool]) -> A | None:
    for x in xs:
        if p(x):
            return x
    return None


def solve(reader: io.TextIOBase) -> int:
    filled = set()
    maxY = 0
    for line in reader.readlines():
        points = [parsePoint(s) for s in line.strip().split(" -> ")]
        for i in range(1, len(points)):
            (x1, y1) = points[i - 1]
            (x2, y2) = points[i]
            if x1 == x2:
                for y in inclRange(y1, y2):
                    filled.add((x1, y))
            if y1 == y2:
                for x in inclRange(x1, x2):
                    filled.add((x, y1))
            maxY = max(maxY, y1, y2)

    count = 0
    while (500, 0) not in filled:
        (x, y) = (500, 0)
        while True:
            dx = findWith(
                [0, -1, 1],
                lambda d: y <= maxY and (x+d, y+1) not in filled,
            )
            if dx is None:
                filled.add((x, y))
                count += 1
                break
            else:
                (x, y) = (x+dx, y+1)

    return count


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"{solution} units of sand come to rest.")


if __name__ == "__main__":
    main()
