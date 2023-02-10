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
EXAMPLE_OUTPUT = 3


@dataclass
class Node:
    value: int
    left: Node
    right: Node


def solve(reader: io.TextIOBase) -> int:
    numbers = []
    for line in reader:
        numbers.append(int(line))
    nodes = [Node(value, None, None) for value in numbers]  # type: ignore
    for (i, node) in enumerate(nodes):
        node.left = nodes[(i - 1) % len(nodes)]
        node.right = nodes[(i + 1) % len(nodes)]

    zero = None
    for node in nodes:
        if node.value == 0:
            zero = node
            continue
        (node.left.right, node.right.left) = (node.right, node.left)
        curr = node
        if node.value > 0:
            for _ in range(node.value):
                curr = curr.right
        else:
            for _ in range(-node.value + 1):
                curr = curr.left
        (node.left, node.right) = (curr, curr.right)
        (curr.right.left, curr.right) = (node, node)

    assert zero is not None

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
