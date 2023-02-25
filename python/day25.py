from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 25
EXAMPLE_INPUT = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
EXAMPLE_OUTPUT = "2=-1=0"


UNIT_TESTS = {
    "1=-0-2": 1747,
    "12111": 906,
    "2=0=": 198,
    "21": 11,
    "2=01": 201,
    "111": 31,
    "20012": 1257,
    "112": 32,
    "1=-1=": 353,
    "1-12": 107,
    "12": 7,
    "1=": 3,
    "122": 37,
}

SNAFU_TO_DECIMAL = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

BASE5_TO_SNAFU: list[tuple[int, str]] = [
    (0, "0"),
    (0, "1"),
    (0, "2"),
    (1, "="),
    (1, "-"),
]


def snafu_to_decimal(snafu: str) -> int:
    result = 0
    for digit in snafu:
        result = 5 * result + SNAFU_TO_DECIMAL[digit]
    return result


def decimal_to_snafu(decimal: int) -> str:
    if decimal == 0:
        return "0"
    reverse_digits = []
    while decimal != 0:
        (q, r) = divmod(decimal, 5)
        (c, d) = BASE5_TO_SNAFU[r]
        reverse_digits.append(d)
        decimal = q + c
    return "".join(reversed(reverse_digits))


for (snafu, decimal) in UNIT_TESTS.items():
    assert snafu_to_decimal(snafu) == decimal,\
        f"snafu_to_decimal({snafu}) == {decimal}"
    assert decimal_to_snafu(decimal) == snafu,\
        f"decimal_to_snafu({decimal}) == {snafu}"


def solve(reader: io.TextIOBase) -> str:
    return decimal_to_snafu(sum(snafu_to_decimal(line.strip()) for line in reader))


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"{solution}")


if __name__ == "__main__":
    main()
