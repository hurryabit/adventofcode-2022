from __future__ import annotations
from dataclasses import dataclass
from functools import cache
import io
import re

DAY = 16
EXAMPLE_INPUT = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
EXAMPLE_OUTPUT = 1651


@dataclass
class Valve:
    name: str
    rate: int
    neighbours: list[str]


def solve(reader: io.TextIOBase) -> int:
    valves = {}
    for line in reader.readlines():
        match = re.match(
            "Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]+(, [A-Z]+)*)",
            line,
        )
        if match is None:
            print(f"cannot parse: {line}")
            continue
        valve = Valve(
            name=match[1],
            rate=int(match[2]),
            neighbours=match[3].split(", "),
        )
        valves[valve.name] = valve

    @cache
    def dp(timeLeft: int, location: str, openedValves: frozenset[str]) -> int:
        if timeLeft == 0:
            return 0

        valve = valves[location]
        open = 0
        if valve.rate > 0 and location not in openedValves:
            open = valve.rate * (timeLeft - 1) \
                + dp(timeLeft - 1, location, openedValves | {location})
        move = max(dp(timeLeft - 1, neighbour, openedValves)
                   for neighbour in valve.neighbours)

        return max(open, move)

    return dp(30, "AA", frozenset())


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"At most {solution} pressure can be released.")


if __name__ == "__main__":
    main()
