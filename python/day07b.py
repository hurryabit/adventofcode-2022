from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass
import io
import re

EXAMPLE_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@dataclass
class File:
    name: str
    size: int

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


@dataclass
class Directory:
    name: str
    children: list[Directory | File]
    size: int

    def __init__(self, name: str):
        self.name = name
        self.children = []
        self.size = 0


def updateSizes(item: Directory | File) -> int:
    match item:
        case File(_, _):
            return item.size
        case Directory(_, _, _):
            total = sum(map(updateSizes, item.children))
            item.size = total
            return total


def parseLog(lines: list[str]) -> Directory:
    root = Directory("/")
    current = root
    path: list[Directory] = []

    for line in lines:
        match line.strip().split():
            case ["$", "cd", "/"]:
                current = root
                path = []
            case ["$", "cd", ".."]:
                current = path.pop()
            case ["$", "cd", name]:
                dir = None
                for child in current.children:
                    if isinstance(child, Directory) and child.name == name:
                        dir = child
                if dir is None:
                    print(f"cannot cd into {name}")
                assert dir is not None
                path.append(current)
                current = dir
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                current.children.append(Directory(name))
            case [size, name]:
                current.children.append(File(name, int(size)))
    return root


def walk(dir: Directory) -> Iterator[Directory]:
    yield dir
    for child in dir.children:
        if isinstance(child, Directory):
            yield from walk(child)


def solve(reader: io.TextIOBase) -> int:
    root = parseLog(reader.readlines())
    updateSizes(root)
    free = 70_000_000 - root.size
    bestFree = 70_000_000
    bestDir = root

    for dir in walk(root):
        if 30_000_000 <= free + dir.size < bestFree:
            bestFree = free + dir.size
            bestDir = dir

    return bestDir.size


assert solve(io.StringIO(EXAMPLE_INPUT)) == 24933642


def main():
    with open("input/day07.txt") as file:
        solution = solve(file)
        print(f"The smallest dir has size {solution}.")


if __name__ == "__main__":
    main()
