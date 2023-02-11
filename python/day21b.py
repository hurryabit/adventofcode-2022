from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
from math import gcd
from typing import ClassVar, overload
import io


@dataclass
class Ratio:
    _numer: int
    _denom: int

    def __init__(self, numer: int, denom: int = 1):
        if denom == 0:
            raise ZeroDivisionError

        d = gcd(numer, denom)
        numer //= d
        denom //= d
        if denom < 0:
            (numer, denom) = (-numer, -denom)
        (self._numer, self._denom) = (numer, denom)

    def __str__(self) -> str:
        return f"{self._numer}/{self._denom}" if self._denom > 1 else f"{self._numer}"

    def __add__(self, other: Ratio):
        return Ratio(
            self._numer * other._denom + other._numer * self._denom,
            self._denom * other._denom,
        )

    def __sub__(self, other: Ratio):
        return Ratio(
            self._numer * other._denom - other._numer * self._denom,
            self._denom * other._denom,
        )

    def __mul__(self, other: Ratio):
        return Ratio(self._numer * other._numer, self._denom * other._denom)

    def __truediv__(self, other: Ratio):
        return Ratio(self._numer * other._denom, self._denom * other._numer)


assert Ratio(6, 3) == Ratio(4, 2)
assert Ratio(1, 2) + Ratio(1, 3) == Ratio(5, 6)
assert Ratio(1, 2) - Ratio(1, 3) == Ratio(1, 6)
assert Ratio(1, 3) * Ratio(1, 2) == Ratio(1, 6)
assert Ratio(1, 3) / Ratio(1, 2) == Ratio(2, 3)


@dataclass
class Polynomial:
    _coefficients: tuple[Ratio]

    X: ClassVar[Polynomial] = None  # type: ignore

    @overload
    def __init__(self, _: Iterable[Ratio | int]):
        pass

    @overload
    def __init__(self, _: Ratio | int, *args: Ratio | int):
        pass

    def __init__(self, _: Iterable[Ratio | int] | Ratio | int, *args: Ratio | int):
        if isinstance(_, Iterable):
            assert len(args) == 0
            coefficients = list(_)
        else:
            assert isinstance(_, Ratio) or isinstance(_, int)
            coefficients = [_] + list(args)
        coefficients = [c if isinstance(c, Ratio) else Ratio(c)
                        for c in coefficients]
        while len(coefficients) > 0 and coefficients[-1] == Ratio(0):
            coefficients.pop()
        self._coefficients = tuple(coefficients)

    def __len__(self) -> int:
        return len(self._coefficients)

    def __getitem__(self, i: int) -> Ratio:
        return self._coefficients[i] if i < len(self) else Ratio(0)

    def __str__(self) -> str:
        monoms = []
        for (i, c) in enumerate(self._coefficients):
            if c == Ratio(0):
                continue
            if i == 0:
                monoms.append(f"{c}")
            else:
                power = "X" if i == 1 else f"X^{i}"
                if c == Ratio(1):
                    monoms.append(power)
                else:
                    monoms.append(f"{c}{power}")
        if len(monoms) == 0:
            return "0"
        return "+".join(reversed(monoms))

    def __add__(self, other: Polynomial) -> Polynomial:
        n = max(len(self), len(other))
        return Polynomial(self[i] + other[i] for i in range(n))

    def __sub__(self, other: Polynomial) -> Polynomial:
        n = max(len(self), len(other))
        return Polynomial(self[i] - other[i] for i in range(n))

    def __mul__(self, other: Polynomial) -> Polynomial:
        n = len(self) + len(other) - 1
        return Polynomial(sum((self[i] * other[k - i] for i in range(k + 1)), start=Ratio(0))
                          for k in range(n))

    def __truediv__(self, other: Polynomial) -> Polynomial:
        if len(other) != 1:
            raise ValueError(f"cannot divide by polynomial ${other}")
        const = other[0]
        return Polynomial(self[i] / const for i in range(len(self)))


Polynomial.X = Polynomial(0, 1)

assert Polynomial(i for i in range(3)) == Polynomial(0, 1, 2)
assert Polynomial([0, 1, 2]) == Polynomial(0, 1, 2)
assert Polynomial(0) == Polynomial(Ratio(0))

assert Polynomial(0, 1, 2) + Polynomial(3, 4) == Polynomial(3, 5, 2)
assert Polynomial(0, 1, 2) + Polynomial(1, 0, -2) == Polynomial(1, 1)
assert Polynomial(0, 1, 2) - Polynomial(3, 4) == Polynomial(-3, -3, 2)
assert Polynomial(0, 1, 2) - Polynomial(1, 0, 2) == Polynomial(-1, 1)
assert Polynomial(1, 1) * Polynomial(1, 1, 1) == Polynomial(1, 2, 2, 1)
assert Polynomial(4, 2) / Polynomial(2) == Polynomial(2, 1)


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
EXAMPLE_OUTPUT = Ratio(301)


def solve(reader: io.TextIOBase) -> Ratio:
    monkeys: dict[str, str] = {}
    for line in reader:
        monkeys[line[:4]] = line[6:].strip()

    def eval(name: str) -> Polynomial:
        if name == "humn":
            return Polynomial.X
        expr = monkeys[name]
        match expr.split():
            case [num]: return Polynomial(int(num))
            case [left, op, right]:
                match op:
                    case "+": return eval(left) + eval(right)
                    case "-": return eval(left) - eval(right)
                    case "*": return eval(left) * eval(right)
                    case "/": return eval(left) / eval(right)
                    case _: raise Exception(f"bad operator: {op}")
            case _: raise Exception(f"bad expression: {expr}")

    [left, _, right] = monkeys["root"].split()
    diff = eval(left) - eval(right)
    assert len(diff) <= 2
    solution = (Ratio(0) - diff[0]) / diff[1]
    return solution


assert solve(io.StringIO(EXAMPLE_INPUT)) == EXAMPLE_OUTPUT


def main():
    with open(f"input/day{DAY}.txt") as file:
        solution = solve(file)
        print(f"I need to yell {solution}.")


if __name__ == "__main__":
    main()
