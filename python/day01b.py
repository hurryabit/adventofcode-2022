import math


def main():
    with open("input/day01.txt") as file:
        sums = []
        current_sum = 0
        for line in file.readlines():
            line = line.strip()
            if line == "":
                sums.append(current_sum)
                current_sum = 0
            else:
                current_sum += int(line)
        sums.append(current_sum)
        sums.sort(reverse=True)
        result = sum(sums[:3])
        print(f"The Elves are carrying {result} Calories.")


if __name__ == "__main__":
    main()
