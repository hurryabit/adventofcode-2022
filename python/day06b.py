import io
import re

EXAMPLE_INPUT = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


def solve(data):
    for i in range(len(data) - 3):
        if len(set(data[i:i+14])) == 14:
            return i + 14


assert solve(EXAMPLE_INPUT) == 19


def main():
    with open("input/day06.txt") as file:
        solution = solve(file.read())
        print(f"The first marker is after character {solution}.")


if __name__ == "__main__":
    main()
