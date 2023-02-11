from __future__ import annotations
from dataclasses import dataclass
import io
import re

DAY = 21
EXAMPLE_INPUT = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
EXAMPLE_OUTPUT = 152


def solve(reader: io.TextIOBase) -> int:
    monkeys: dict[str, str] = {}
    for line in reader:
        monkeys[line[:4]] = line[6:].strip()

    def eval(name: str) -> int:
        expr = monkeys[name]
        match expr.split():
            case [num]: return int(num)
            case [left, op, right]:
                match op:
                    case "+": return eval(left) + eval(right)
                    case "-": return eval(left) - eval(right)
                    case "*": return eval(left) * eval(right)
                    case "/": return eval(left) // eval(right)
                    case _: raise Exception(f"bad operator: {op}")
            case _: raise Exception(f"bad expression: {expr}")

    return eval("root")


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"{solution}")


if __name__ == "__main__":
    main()
