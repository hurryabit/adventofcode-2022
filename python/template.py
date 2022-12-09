from __future__ import annotations
from dataclasses import dataclass
import io
import re

EXAMPLE_INPUT = """"""


def solve(reader: io.TextIOBase) -> int:
    return 0


assert solve(io.StringIO(EXAMPLE_INPUT)) == 0


def main():
    with open("input/day??.txt") as file:
        solution = solve(file)
        print(f"{solution}")


if __name__ == "__main__":
    main()
