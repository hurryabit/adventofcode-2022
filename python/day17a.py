from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 17
EXAMPLE_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
EXAMPLE_OUTPUT = 3068

ROUNDS = 2022

TILES = [
    ["####"],
    [" # ", "###", " # "],
    ["###", "  #", "  #"],
    ["#", "#", "#", "#"],
    ["##", "##"],
]

DELTAS = {"<": -1, ">": 1}


def fits(board: list[list[str]], tile: list[str], anchorX: int, anchorY: int) -> bool:
    return all(board[anchorY + y][anchorX + x] != "#" or tile[y][x] != "#"
               for y in range(len(tile)) for x in range(len(tile[y])))


def solve(dirs: str) -> int:
    board = [list(9 * "#")] + [list("#       #")
                               for _ in range(5 * ROUNDS + 10)]
    maxY = 0

    dirIndex = 0
    tileIndex = 0
    for _ in range(ROUNDS):
        tile = TILES[tileIndex]
        tileIndex = (tileIndex + 1) % len(TILES)
        anchorX = 3
        anchorY = maxY + 4

        while True:
            dir = dirs[dirIndex]
            dirIndex = (dirIndex + 1) % len(dirs)
            dx = DELTAS[dir]

            if fits(board, tile, anchorX + dx, anchorY):
                anchorX += dx

            if fits(board, tile, anchorX, anchorY - 1):
                anchorY -= 1
            else:
                break

        for y in range(len(tile)):
            for x in range(len(tile[y])):
                if tile[y][x] == "#":
                    board[anchorY + y][anchorX + x] = "#"
                    maxY = max(maxY, anchorY + y)

    return maxY


assert solve(EXAMPLE_INPUT) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file.read().strip())
        print(f"The tower will be {solution} units tall.")


if __name__ == "__main__":
    main()
