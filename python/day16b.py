from __future__ import annotations
from collections import deque
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
EXAMPLE_OUTPUT = 1707

START = "AA"
INITIAL_TIME = 26


def solve(reader: io.TextIOBase) -> int:
    rates = {}
    adjacency = {}
    for line in reader.readlines():
        match = re.match(
            "Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]+(, [A-Z]+)*)",
            line,
        )
        name = match.group(1)
        rate = int(match.group(2))
        if rate > 0:
            rates[name] = rate
        adjacency[name] = match.group(3).split(", ")

    distances = {}
    for start in [START] + list(rates):
        distances[start] = []
        seen = {start}
        queue = deque([(start, 0)])
        while len(queue) > 0:
            (node, dist) = queue.popleft()
            for neighbour in adjacency[node]:
                if neighbour in seen:
                    continue
                seen.add(neighbour)
                queue.append((neighbour, dist + 1))
                if neighbour in rates:
                    distances[start].append((neighbour, dist + 1))

    @cache
    def dp(time: int, node: str, seen: frozenset[str], reboot: bool) -> int:
        result = max(
            (rates[neighbour] * (time - dist - 1) + dp(time - dist - 1, neighbour, seen | {neighbour}, reboot)
                for (neighbour, dist) in distances[node] if neighbour not in seen and dist + 1 < time),
            default=0,
        )
        if reboot:
            result = max(result, dp(INITIAL_TIME, START, seen, False))
        return result

    return dp(INITIAL_TIME, START, frozenset(), True)


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"At most {solution} pressure can be released.")


if __name__ == "__main__":
    main()
