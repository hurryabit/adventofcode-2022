from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 100
EXAMPLE_INPUT = """"""
EXAMPLE_OUTPUT = 0


def solve(reader: io.TextIOBase) -> int:
    return 0


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"{solution}")


if __name__ == "__main__":
    main()
