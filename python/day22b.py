from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import io
import re

DAY = 22
EXAMPLE_INPUT = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
EXAMPLE_OUTPUT = 5031


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Position) -> Position:
        return Position(self.row - other.row, self.col - other.col)

    def __rmul__(self, scale: int) -> Position:
        return Position(scale * self.row, scale * self.col)


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn_right(self) -> Direction:
        return Direction((self.value + 1) % len(Direction))

    def turn_left(self) -> Direction:
        return Direction((self.value - 1) % len(Direction))

    def turn_around(self) -> Direction:
        return Direction((self.value + 2) % len(Direction))

    def delta(self) -> Position:
        match self:
            case Direction.RIGHT: return Position(0, 1)
            case Direction.DOWN: return Position(1, 0)
            case Direction.LEFT: return Position(0, -1)
            case Direction.UP: return Position(-1, 0)


assert Direction.RIGHT.turn_right() == Direction.DOWN
assert Direction.UP.turn_right() == Direction.RIGHT
assert Direction.RIGHT.turn_left() == Direction.UP
assert Direction.DOWN.turn_left() == Direction.RIGHT


# Cube:       Unfolding:
#             Problem       Example
#   A----B       A--B--F          A--B
#  /|   /|       |  |  |          |  |
# D----C |       D--C--G    B--A--D--C
# | |  | |       |  |       |  |  |  |
# | E--|-F    D--H--G       F--E--H--G--C
# |/   |/     |  |  |             |  |  |
# H----G      A--E--F             E--F--B
#             |  |
#             B--F

Cut = tuple[Position, Direction, Position, Direction]

EXAMPLE_LENGTH = 4
EXAMPLE_CUTS = [
    (Position(0, 8), Direction.RIGHT, Position(4, 3), Direction.LEFT),  # A--B
    (Position(0, 11), Direction.DOWN, Position(11, 15), Direction.UP),  # B--C
    (Position(4, 11), Direction.DOWN, Position(8, 15), Direction.LEFT),  # C--G
    (Position(11, 15), Direction.LEFT, Position(4, 0), Direction.DOWN),  # B--F
    (Position(11, 11), Direction.LEFT, Position(7, 0), Direction.RIGHT),  # F--E
    (Position(11, 8), Direction.UP, Position(7, 4), Direction.RIGHT),  # E--H
    (Position(4, 4), Direction.RIGHT, Position(0, 8), Direction.DOWN),  # A--D
]

PROBLEM_LENGTH = 50
PROBLEM_CUTS = [
    (Position(0, 50), Direction.RIGHT, Position(150, 0), Direction.DOWN),  # A--B
    (Position(0, 100), Direction.RIGHT, Position(199, 0), Direction.RIGHT),  # B--F
    (Position(0, 149), Direction.DOWN, Position(149, 99), Direction.UP),  # F--G
    (Position(49, 149), Direction.LEFT, Position(99, 99), Direction.UP),  # G--C
    (Position(149, 99), Direction.LEFT, Position(199, 49), Direction.UP),  # F--E
    (Position(149, 0), Direction.UP, Position(0, 50), Direction.DOWN),  # A--D
    (Position(100, 0), Direction.RIGHT, Position(50, 50), Direction.DOWN),  # D--H
]


@dataclass
class Map:
    map: list[str]
    borders: dict[tuple[Position, Direction], tuple[Position, Direction]]
    trace: dict[Position, Direction]

    def __init__(self, map: list[str], length: int, cuts: list[Cut]):
        self.map = map
        self.borders = {}

        for (base1, dir1, base2, dir2) in cuts:
            out1 = dir1.turn_left() if self[base1 + dir1.turn_left().delta()] == " " \
                else dir1.turn_right()
            assert self[base1 + out1.delta()] == " "
            out2 = dir2.turn_left() if self[base2 + dir2.turn_left().delta()] == " " \
                else dir2.turn_right()
            assert self[base2 + out2.delta()] == " "

            for i in range(length):
                pos1 = base1 + i * dir1.delta()
                pos2 = base2 + i * dir2.delta()
                self.borders[(pos1, out1)] = (pos2, out2.turn_around())
                self.borders[(pos2, out2)] = (pos1, out1.turn_around())

        assert len(self.borders) == 14 * length

    def __getitem__(self, pos: Position) -> str:
        c = " "
        if 0 <= pos.row < len(self.map) and 0 <= pos.col < len(self.map[pos.row]):
            c = self.map[pos.row][pos.col]
        if c == "\n":
            c = " "
        assert c in " .#"
        return c

    def start(self) -> Position:
        return Position(0, self.map[0].index("."))

    def move(self, pos: Position, dir: Direction) -> tuple[Position, Direction]:
        assert self[pos] == "."
        (next_pos, next_dir) = self.borders[(pos, dir)] if (pos, dir) in self.borders \
            else (pos + dir.delta(), dir)
        match self[next_pos]:
            case ".": return (next_pos, next_dir)
            case "#": return (pos, dir)
            case " ": raise Exception(f"fell off cube from {pos}/{dir}")
            case c: raise Exception(f"invalid map character: {c}")


def solve(reader: io.TextIOBase, length: int, cuts: list[Cut]) -> int:
    lines = reader.readlines()
    instrs = lines.pop().strip()
    lines.pop()
    map = Map(lines, length, cuts)

    pos = map.start()
    dir = Direction.RIGHT

    while len(instrs) > 0:
        m = re.search("L|R", instrs)
        start = m.start() if m is not None else len(instrs)
        if start > 0:
            count = int(instrs[:start])
            for _ in range(count):
                (pos, dir) = map.move(pos, dir)
            instrs = instrs[start:]
        else:
            match instrs[0]:
                case "L":
                    dir = dir.turn_left()
                case "R":
                    dir = dir.turn_right()
                case d:
                    raise Exception(f"invalid direction: {d}")
            instrs = instrs[1:]

    return 1000 * (pos.row + 1) + 4 * (pos.col + 1) + dir.value


assert solve(io.StringIO(EXAMPLE_INPUT), EXAMPLE_LENGTH,
             EXAMPLE_CUTS) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file, PROBLEM_LENGTH, PROBLEM_CUTS)
        print(f"The final password is {solution}.")


if __name__ == "__main__":
    main()
