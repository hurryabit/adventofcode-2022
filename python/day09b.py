from __future__ import annotations
from dataclasses import dataclass
import io

EXAMPLE_INPUT = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


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
    rope = 10 * [Point(0, 0)]
    visited = {rope[-1]}

    for line in reader.readlines():
        [dir, steps] = line.split()
        for _ in range(int(steps)):
            rope[0] = rope[0].move(dir)
            for i in range(1, len(rope)):
                dist = rope[i - 1] - rope[i]
                if dist.max_norm() >= 2:
                    rope[i] = rope[i] + dist.sign()
            visited.add(rope[-1])

    return len(visited)


assert solve(io.StringIO(EXAMPLE_INPUT)) == 36


def main():
    with open("input/day09.txt") as file:
        solution = solve(file)
        print(f"The tail visits {solution} positions.")


if __name__ == "__main__":
    main()
