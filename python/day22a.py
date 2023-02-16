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
EXAMPLE_OUTPUT = 6032


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Position) -> Position:
        return Position(self.row - other.row, self.col - other.col)


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn_right(self) -> Direction:
        return Direction((self.value + 1) % len(Direction))

    def turn_left(self) -> Direction:
        return Direction((self.value - 1) % len(Direction))

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


@dataclass
class Map:
    map: list[str]

    def __getitem__(self, pos: Position) -> str:
        c = " "
        if 0 <= pos.row < len(self.map) and 0 <= pos.col < len(self.map[pos.row]):
            c = self.map[pos.row][pos.col]
        if c == "\n":
            c = " "
        assert c in " .#"
        return c

    def move(self, pos: Position, dir: Direction) -> Position:
        assert self[pos] == "."
        delta = dir.delta()
        match self[pos + delta]:
            case ".": return pos + delta
            case "#": return pos
            case " ":
                curr = pos
                while self[curr - delta] != " ":
                    curr = curr - delta
                match self[curr]:
                    case ".": return curr
                    case "#": return pos
                    case c: raise Exception(f"invalid map character: {c}")
            case c: raise Exception(f"invalid map character: {c}")


def solve(reader: io.TextIOBase) -> int:
    lines = reader.readlines()
    instrs = lines.pop().strip()
    lines.pop()
    map = Map(lines)

    pos = Position(0, lines[0].index("."))
    dir = Direction.RIGHT

    while len(instrs) > 0:
        m = re.search("L|R", instrs)
        start = m.start() if m is not None else len(instrs)
        if start > 0:
            count = int(instrs[:start])
            for _ in range(count):
                pos = map.move(pos, dir)
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


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The final password is {solution}.")


if __name__ == "__main__":
    main()
