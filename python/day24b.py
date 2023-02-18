from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
import io

DAY = 24
EXAMPLE_INPUT = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
EXAMPLE_OUTPUT = 54


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Position) -> Position:
        return Position(self.row - other.row, self.col - other.col)

    def __mod__(self, other: Position) -> Position:
        return Position(self.row % other.row, self.col % other.col)

    def __rmul__(self, scale: int) -> Position:
        return Position(scale * self.row, scale * self.col)


class Direction(Enum):
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    UP = auto()

    @classmethod
    def from_arrow(cls, c: str) -> Direction:
        match c:
            case ">": return cls.RIGHT
            case "v": return cls.DOWN
            case "<": return cls.LEFT
            case "^": return cls.UP
            case c: raise Exception(f"invalid direction: {c}")

    def delta(self) -> Position:
        match self:
            case Direction.RIGHT: return Position(0, 1)
            case Direction.DOWN: return Position(1, 0)
            case Direction.LEFT: return Position(0, -1)
            case Direction.UP: return Position(-1, 0)


def solve(reader: io.TextIOBase) -> int:
    map = [line.strip() for line in reader]
    dim = Position(len(map), len(map[0]))

    blizzards: dict[Position, list[Direction]] = defaultdict(list)
    for (row, line) in enumerate(map):
        for (col, char) in enumerate(line):
            if char in ">v<^":
                blizzards[Position(row, col)].\
                    append(Direction.from_arrow(char))

    round = 0
    leg = 1
    entrance = Position(0, 1)
    exit = dim - Position(1, 2)
    positions = {entrance}

    while True:
        round += 1

        new_blizzards = defaultdict(list)
        for (blizzard, dirs) in blizzards.items():
            for dir in dirs:
                target = blizzard + dir.delta()
                if map[target.row][target.col] == "#":
                    target = (target + 2 * dir.delta()) % dim
                new_blizzards[target].append(dir)
        blizzards = new_blizzards

        new_positions = set()
        for pos in positions:
            new_positions.add(pos)
            for dir in list(Direction):
                target = pos + dir.delta()
                if 0 <= target.row < dim.row and map[target.row][target.col] != "#":
                    new_positions.add(target)
        positions = {pos for pos in new_positions if pos not in blizzards}

        if leg == 1 and exit in positions:
            leg = 2
            positions = {exit}
        elif leg == 2 and entrance in positions:
            leg = 3
            positions = {entrance}
        elif leg == 3 and exit in positions:
            return round


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The quickest way takes {solution} minutes.")


if __name__ == "__main__":
    main()
