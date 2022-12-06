import io
import re

EXAMPLE_INPUT = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def solve(reader: io.TextIOBase) -> str:
    lines = reader.readlines()
    pivot = lines.index("\n")

    crates = [[] for _ in lines[pivot - 1].split()]

    for line in reversed(lines[:pivot - 1]):
        for i in range(len(crates)):
            if 4 * i + 1 < len(line):
                c = line[4 * i + 1]
                if c != " ":
                    crates[i].append(c)

    for line in lines[pivot + 1:]:
        match = re.match("move (\d+) from (\d+) to (\d+)", line)
        (count, from_, to) = tuple(map(int, match.groups()))
        for _ in range(count):
            crates[to - 1].append(crates[from_ - 1].pop())

    return "".join(map(lambda crate: crate[-1], crates))


assert solve(io.StringIO(EXAMPLE_INPUT)) == "CMZ"


def main():
    with open("input/day05.txt") as file:
        solution = solve(file)
        print(f"The top crates are {solution}.")


if __name__ == "__main__":
    main()
