#! /usr/bin/env python3

from common import *


convert_to_int = lambda x: int(x) if x else None

class Day01(Puzzle):

    def parse_data(self, filename) -> list:
        numbers = map(convert_to_int, super().parse_data(filename))

        snacks = [0]
        for n in numbers:
            if n:
                snacks[-1] += n
            else:
                snacks.append(0)

        return snacks

    def part1(self, data) -> int:
        return max(data)

    def part2(self, data) -> int:
        data.sort()
        return sum(data[-3:])

puzzle = Day01()
puzzle.run(24000, 45000)
