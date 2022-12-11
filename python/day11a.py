from __future__ import annotations
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
import math


@dataclass
class Monkey:
    items: deque[int]
    operation: Callable[[int], int]
    test: int
    trueTarget: int
    falseTarget: int
    count: int = 0


EXAMPLE_MONKEYS = [
    Monkey(
        items=deque([79, 98]),
        operation=lambda old: old * 19,
        test=23,
        trueTarget=2,
        falseTarget=3,
    ),
    Monkey(
        items=deque([54, 65, 75, 74]),
        operation=lambda old: old + 6,
        test=19,
        trueTarget=2,
        falseTarget=0,
    ),
    Monkey(
        items=deque([79, 60, 97]),
        operation=lambda old: old * old,
        test=13,
        trueTarget=1,
        falseTarget=3,
    ),
    Monkey(
        items=deque([74]),
        operation=lambda old: old + 3,
        test=17,
        trueTarget=0,
        falseTarget=1,
    ),
]

INPUT_MONKEYS = [
    Monkey(
        items=deque([54, 61, 97, 63, 74]),
        operation=lambda old: old * 7,
        test=17,
        trueTarget=5,
        falseTarget=3,
    ),
    Monkey(
        items=deque([61, 70, 97, 64, 99, 83, 52, 87]),
        operation=lambda old: old + 8,
        test=2,
        trueTarget=7,
        falseTarget=6,
    ),
    Monkey(
        items=deque([60, 67, 80, 65]),
        operation=lambda old: old * 13,
        test=5,
        trueTarget=1,
        falseTarget=6,
    ),
    Monkey(
        items=deque([61, 70, 76, 69, 82, 56]),
        operation=lambda old: old + 7,
        test=3,
        trueTarget=5,
        falseTarget=2,
    ),
    Monkey(
        items=deque([79, 98]),
        operation=lambda old: old + 2,
        test=7,
        trueTarget=0,
        falseTarget=3,
    ),
    Monkey(
        items=deque([72, 79, 55]),
        operation=lambda old: old + 1,
        test=13,
        trueTarget=2,
        falseTarget=1,
    ),
    Monkey(
        items=deque([63]),
        operation=lambda old: old + 4,
        test=19,
        trueTarget=7,
        falseTarget=4,
    ),
    Monkey(
        items=deque([72, 51, 93, 63, 80, 86, 81]),
        operation=lambda old: old * old,
        test=11,
        trueTarget=0,
        falseTarget=4,
    ),
]


def businessLevel(monkeys: list[Monkey]) -> int:
    for _ in range(20):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.count += 1
                item = monkey.items.popleft()
                item = monkey.operation(item) // 3
                target = monkey.trueTarget if item % monkey.test == 0 else monkey.falseTarget
                monkeys[target].items.append(item)

    counts = [m.count for m in monkeys]
    counts.sort(reverse=True)
    return math.prod(counts[:2])


assert businessLevel(EXAMPLE_MONKEYS) == 10605


def main():
    business = businessLevel(INPUT_MONKEYS)
    print(f"The level of monkey business is {business}.")


if __name__ == "__main__":
    main()
