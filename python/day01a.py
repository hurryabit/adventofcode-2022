import math


def main():
    with open("input/day01.txt") as file:
        result = 0
        sum = 0
        for line in file.readlines():
            line = line.strip()
            if line == "":
                result = max(result, sum)
                sum = 0
            else:
                sum += int(line)
        result = max(result, sum)
        print(f"The Elf is carrying {result} Calories.")


if __name__ == "__main__":
    main()
