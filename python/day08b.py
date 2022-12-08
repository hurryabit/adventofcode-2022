from collections.abc import Iterator
import io

EXAMPLE_INPUT = """30373
25512
65332
33549
35390"""


def dirScore(height: int, view: Iterator[int]) -> int:
    score = 0
    for h in view:
        score += 1
        if h >= height:
            break
    return score


def solve(reader: io.TextIOBase) -> str:
    matrix = list(map(
        lambda row: list(map(int, row.strip())),
        reader.readlines(),
    ))
    maxScore = 0

    for (i, row) in enumerate(matrix):
        for (j, height) in enumerate(row):
            score = dirScore(height, reversed(row[:j])) \
                * dirScore(height, row[j + 1:]) \
                * dirScore(height, map(lambda k: matrix[k][j], reversed(range(i)))) \
                * dirScore(height, map(lambda k: matrix[k][j], range(i + 1, len(matrix))))
            maxScore = max(maxScore, score)

    return maxScore


assert solve(io.StringIO(EXAMPLE_INPUT)) == 8


def main():
    with open("input/day08.txt") as file:
        solution = solve(file)
        print(f"The highest scenic score is {solution}.")


if __name__ == "__main__":
    main()
