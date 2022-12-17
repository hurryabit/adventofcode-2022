from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 17
EXAMPLE_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
EXAMPLE_OUTPUT = 1514285714288

ROUNDS = 1_000_000_000_000

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
    board = [list(9 * "#")]
    maxY = 0
    extraY = 0
    seen = {}

    dirIndex = 0
    tileIndex = 0
    round = 0
    while round < ROUNDS:
        round += 1
        # print(f"Round {round}")
        tile = TILES[tileIndex]
        tileIndex = (tileIndex + 1) % len(TILES)
        anchorX = 3
        anchorY = maxY + 4
        board.extend(list("#       #")
                     for _ in range(anchorY + len(tile) - len(board)))

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

        if extraY > 0 or maxY < 10:
            continue

        top = "".join(c for dy in range(10) for c in board[maxY - dy])
        state = (tileIndex, dirIndex, top)
        if state in seen:
            (oldRound, oldMaxY) = seen[state]
            cycleLen = round - oldRound
            print(f"Detected cycle of length {cycleLen} after {round} rounds.")
            skipCycles = (ROUNDS - round) // cycleLen
            round += skipCycles * cycleLen
            extraY = skipCycles * (maxY - oldMaxY)
        else:
            seen[state] = (round, maxY)

    return maxY + extraY


assert solve(EXAMPLE_INPUT) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file.read().strip())
        print(f"The tower will be {solution} units tall.")


if __name__ == "__main__":
    main()
