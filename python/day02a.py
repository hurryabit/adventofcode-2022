import math


SCORES = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6,
}


def main():
    with open("input/day02.txt") as file:
        total = 0
        for line in file.readlines():
            line = line.strip()
            total += SCORES[line]
        print(f"My total score would be {total}.")


if __name__ == "__main__":
    main()
