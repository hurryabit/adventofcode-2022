import io

EXAMPLE_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def digits_to_int(digits, base=10):
    result = 0
    for digit in digits:
        result = base * result + digit
    return result


def solve(reader):
    total = 0
    group_size = 0
    for line in reader.readlines():
        line = line.strip()
        if group_size == 0:
            common_items = set(line)
        else:
            common_items &= set(line)
        group_size += 1
        if group_size == 3:
            common = next(iter(common_items))
            if "a" <= common <= "z":
                priority = ord(common) - ord("a") + 1
            else:
                priority = ord(common) - ord("A") + 27
            total += priority
            group_size = 0
    return total


assert solve(io.StringIO(EXAMPLE_INPUT)) == 70


def main():
    with open("input/day03.txt") as file:
        solution = solve(file)
        print(f"The sum of the priorities is {solution}.")


if __name__ == "__main__":
    main()
