import io

EXAMPLE_INPUT = """30373
25512
65332
33549
35390"""


def solve(reader: io.TextIOBase) -> str:
    matrix = list(map(
        lambda row: list(map(int, row.strip())),
        reader.readlines(),
    ))
    total = 0

    for (i, row) in enumerate(matrix):
        for (j, cell) in enumerate(row):
            isVisible = all(map(lambda k: row[k] < cell, range(j))) \
                or all(map(lambda k: row[k] < cell, range(j + 1, len(row)))) \
                or all(map(lambda k: matrix[k][j] < cell, range(i))) \
                or all(map(lambda k: matrix[k][j] < cell, range(i + 1, len(matrix))))
            if isVisible:
                total += 1

    return total


assert solve(io.StringIO(EXAMPLE_INPUT)) == 21


def main():
    with open("input/day08.txt") as file:
        solution = solve(file)
        print(f"{solution} trees are visible.")


if __name__ == "__main__":
    main()
