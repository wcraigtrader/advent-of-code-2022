#! /usr/bin/env python3

from common import *
from itertools import zip_longest
from functools import cmp_to_key


def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


class Day13(Puzzle):
    """Distress Signal"""

    def parse_data(self, filename):
        lines = self.read_stripped(filename)
        return [[
                eval(lines[i]),
                eval(lines[i + 1])]
                for i in range(0, len(lines), 3)]

    def compare(self, left: list | int, right: list | int) -> int:
        """Compare nested lists of integers"""

        if isinstance(left, int) and isinstance(right, int):
            return cmp(left, right)

        if isinstance(left, list) and isinstance(right, int):
            return self.compare(left, [right])

        if isinstance(left, int) and isinstance(right, list):
            return self.compare([left], right)

        for l, r in zip_longest(left, right):
            if l is None:
                return -1
            elif r is None:
                return 1
            else:
                test = self.compare(l, r)
                if test != 0:
                    return test

        return 0

    def part1(self, data) -> int:
        total = 0
        for index, (left, right) in enumerate(data, 1):
            result = self.compare(left, right)
            total += index if result <= 0 else 0
        return total

    def part2(self, data) -> int:
        markers = [[[2]], [[6]], ]

        packets = []
        for left, right in data:
            packets.append(left)
            packets.append(right)
        packets.extend(markers)

        packets.sort(key=cmp_to_key(self.compare))

        decoder = 1
        for index, packet in enumerate(packets, 1):
            if packet in markers:
                decoder *= index

        return decoder


puzzle = Day13()
puzzle.run(13, 140)
