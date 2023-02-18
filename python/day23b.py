from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from enum import Enum
import io

DAY = 23
EXAMPLE_INPUT = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
EXAMPLE_OUTPUT = 20


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Position) -> Position:
        return Position(self.row - other.row, self.col - other.col)


DELTAS = [Position(row, col)
          for row in [-1, 0, 1] for col in [-1, 0, 1] if row != 0 or col != 0]

assert len(DELTAS) == 8


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def turn_right(self) -> Direction:
        return Direction((self.value + 1) % len(Direction))

    def turn_left(self) -> Direction:
        return Direction((self.value - 1) % len(Direction))

    def delta(self) -> Position:
        match self:
            case Direction.NORTH: return Position(-1, 0)
            case Direction.EAST: return Position(0, 1)
            case Direction.SOUTH: return Position(1, 0)
            case Direction.WEST: return Position(0, -1)


assert Direction.NORTH.turn_right() == Direction.EAST
assert Direction.WEST.turn_right() == Direction.NORTH
assert Direction.NORTH.turn_left() == Direction.WEST
assert Direction.EAST.turn_left() == Direction.NORTH


def can_move(elf: Position, dir: Direction, elves: set[Position]) -> bool:
    target = elf + dir.delta()
    return elves.isdisjoint({target, target + dir.turn_left().delta(), target + dir.turn_right().delta()})


def solve(reader: io.TextIOBase) -> int:
    elves: set[Position] = set()
    for (row, line) in enumerate(reader):
        for (col, char) in enumerate(line):
            if char == "#":
                elves.add(Position(row, col))

    directions = \
        [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
    round = 0

    while True:
        round += 1
        proposals = {}
        counts = Counter()

        for elf in elves:  # First half
            target = elf
            if any(elf + delta in elves for delta in DELTAS):  # Elf wants to move
                for dir in directions:
                    if can_move(elf, dir, elves):
                        target = elf + dir.delta()
                        break
            proposals[elf] = target
            counts[target] += 1

        elves.clear()
        moved = False
        for (elf, target) in proposals.items():  # Second half
            assert counts[target] >= 1
            if counts[target] == 1:  # Elf moves
                elves.add(target)
                if target != elf:
                    moved = True
            else:  # Elf does not move
                elves.add(elf)

        if not moved:
            break

        directions = directions[1:] + [directions[0]]

    return round


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"Round {solution} is the first round no elf moves.")


if __name__ == "__main__":
    main()
