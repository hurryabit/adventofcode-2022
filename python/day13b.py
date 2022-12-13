from __future__ import annotations
from enum import Enum
from functools import cmp_to_key
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
EXAMPLE_OUTPUT = 140


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
    packets = [[[2]], [[6]]]
    for line in reader.readlines():
        line = line.strip()
        if line != "":
            packets.append(eval(line))

    packets.sort(key=cmp_to_key(lambda x, y: compare(x, y).value))
    index1 = packets.index([[2]]) + 1
    index2 = packets.index([[6]]) + 1

    return index1 * index2


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The decoder key is {solution}.")


if __name__ == "__main__":
    main()
