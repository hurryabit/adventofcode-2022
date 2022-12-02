import math


SCORES = {
    "A X": 3,
    "A Y": 4,
    "A Z": 8,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 2,
    "C Y": 6,
    "C Z": 7,
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
