from collections import deque
from collections.abc import Iterator
import io

DAY = 12
EXAMPLE_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
EXAMPLE_OUTPUT = 29


Point = (int, int)


def height(c: str) -> int:
    match c:
        case "S":
            return ord("a")
        case "E":
            return ord("z")
        case _:
            return ord(c)


def neighbours(matrix: list[str], pos: Point) -> Iterator[Point]:
    m = len(matrix)
    n = len(matrix[0])
    (i0, j0) = pos
    h0 = height(matrix[i0][j0])

    for (di, dj) in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
        (i1, j1) = (i0 + di, j0 + dj)
        if 0 <= i1 < m and 0 <= j1 < n and height(matrix[i1][j1]) >= h0 - 1:
            yield (i1, j1)


def solve(reader: io.TextIOBase) -> int:
    matrix = [line.strip() for line in reader.readlines()]
    start = None
    ends = set()

    for (i, row) in enumerate(matrix):
        for (j, cell) in enumerate(row):
            match cell:
                case "S" | "a":
                    ends.add((i, j))
                case "E":
                    start = (i, j)

    seen = set([start])
    queue = deque([(start, 0)])
    while len(queue) > 0:
        (current, dist) = queue.popleft()
        if current in ends:
            return dist
        for node in neighbours(matrix, current):
            if node not in seen:
                seen.add(node)
                queue.append((node, dist+1))


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"It takes {solution} steps.")


if __name__ == "__main__":
    main()
