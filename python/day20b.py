from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 20
EXAMPLE_INPUT = """1
2
-3
3
-2
0
4"""
EXAMPLE_OUTPUT = 1623178306


@dataclass
class Node:
    value: int
    left: Node
    right: Node


def solve(reader: io.TextIOBase) -> int:
    numbers = []
    for line in reader:
        numbers.append(int(line))
    nodes = [Node(811589153 * value, None, None)  # type: ignore
             for value in numbers]
    zero = None
    for (i, node) in enumerate(nodes):
        if node.value == 0:
            zero = node
        node.left = nodes[(i - 1) % len(nodes)]
        node.right = nodes[(i + 1) % len(nodes)]
    assert zero is not None

    for _ in range(10):
        for node in nodes:
            delta = node.value % (len(nodes) - 1)
            if delta == 0:
                continue
            (node.left.right, node.right.left) = (node.right, node.left)
            curr = node
            for _ in range(delta):
                curr = curr.right
            (node.left, node.right) = (curr, curr.right)
            (curr.right.left, curr.right) = (node, node)

    node = zero
    result = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.right
        result += node.value

    return result


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"The sum of the grove coordinates is {solution}.")


if __name__ == "__main__":
    main()
