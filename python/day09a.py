from __future__ import annotations
from dataclasses import dataclass
import io

EXAMPLE_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def sign(x: int) -> int:
    return 0 if x == 0 else 1 if x > 0 else -1


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def move(self, dir: str) -> Point:
        match dir:
            case "R":
                return Point(self.x + 1, self.y)
            case "U":
                return Point(self.x, self.y + 1)
            case "L":
                return Point(self.x - 1, self.y)
            case "D":
                return Point(self.x, self.y - 1)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def max_norm(self) -> int:
        return max(abs(self.x), abs(self.y))

    def sign(self) -> Point:
        return Point(sign(self.x), sign(self.y))


def solve(reader: io.TextIOBase) -> int:
    head = Point(0, 0)
    tail = Point(0, 0)
    visited = {tail}

    for line in reader.readlines():
        [dir, steps] = line.split()
        for _ in range(int(steps)):
            head = head.move(dir)
            dist = head - tail
            if dist.max_norm() >= 2:
                tail = tail + dist.sign()
                visited.add(tail)

    return len(visited)


assert solve(io.StringIO(EXAMPLE_INPUT)) == 13


def main():
    with open("input/day09.txt") as file:
        solution = solve(file)
        print(f"The tail visits {solution} positions.")


if __name__ == "__main__":
    main()
