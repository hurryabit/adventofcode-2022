from __future__ import annotations
from enum import Enum
import io

DAY = 13
EXAMPLE_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
EXAMPLE_OUTPUT = 13


class Ord(Enum):
    LT = -1
    EQ = 0
    GT = 1


def compare(left, right) -> Ord:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return Ord.LT
            elif left == right:
                return Ord.EQ
            else:
                return Ord.GT
        else:
            return compare([left], right)
    else:
        if isinstance(right, int):
            return compare(left, [right])
        else:
            if len(left) == 0:
                if len(right) == 0:
                    return Ord.EQ
                else:
                    return Ord.LT
            else:
                if len(right) == 0:
                    return Ord.GT
                else:
                    ord = compare(left[0], right[0])
                    if ord != Ord.EQ:
                        return ord
                    else:
                        return compare(left[1:], right[1:])


def solve(reader: io.TextIOBase) -> int:
    lines = reader.readlines()
    index = 1
    total = 0
    while 3 * (index - 1) < len(lines):
        left = eval(lines[3 * (index - 1)])
        right = eval(lines[3 * (index - 1) + 1])

        if compare(left, right) == Ord.LT:
            total += index

        index += 1

    return total


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The indices sum to {solution}.")


if __name__ == "__main__":
    main()
