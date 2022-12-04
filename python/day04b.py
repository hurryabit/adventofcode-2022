import io
import re

EXAMPLE_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def solve(reader):
    count = 0
    for line in reader.readlines():
        match = re.match("(\d+)-(\d+),(\d+)-(\d+)", line)
        (a, b, c, d) = tuple(map(int, match.groups()))
        if a <= c <= b or a <= d <= b or c <= a <= d or c <= b <= d:
            count += 1
    return count


assert solve(io.StringIO(EXAMPLE_INPUT)) == 4


def main():
    with open("input/day04.txt") as file:
        solution = solve(file)
        print(f"In {solution} pairs the ranges overlap.")


if __name__ == "__main__":
    main()
