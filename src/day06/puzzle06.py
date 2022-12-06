#! /usr/bin/env python3

from common import *


class Day06(Puzzle):

    def parse_data(self, filename):
        return self.read_stripped(filename)

    def detect_marker(self, data, length):
        for i in range(length, len(data)):
            marker = data[i - length:i]
            if len(set(marker)) == length:
                return i
        return 0

    def part1(self, data) -> int:
        return self.detect_marker(data, 4)

    def part2(self, data) -> int:
        return self.detect_marker(data, 14)


puzzle = Day06()
puzzle.run([7, 5, 6, 10, 11], [19, 23, 23, 29, 26])
