#! /usr/bin/env python3

from common import *


class Signal:

    def __init__(self, lines: list[str]):
        self.cycle: list[int] = []

        x = 1
        for line in lines:
            tokens = line.split(' ')
            if tokens[0] == 'addx':
                value = int(tokens[1])
                self.cycle.append(x)
                self.cycle.append(x)
                x += int(value)
            elif tokens[0] == 'noop':
                self.cycle.append(x)

    @property
    def signal_strengths(self) -> int:
        times = [20, 60, 100, 140, 180, 220]
        return sum(t * self.cycle[t - 1] for t in times)

    @property
    def image(self) -> str:
        image = ''
        for t, sprite in enumerate(self.cycle):
            pixel = t % 40

            if pixel == 0:
                image += '\n'
            image += '#' if sprite - 1 <= pixel <= sprite + 1 else '.'

        return image


class Day10(Puzzle):

    def parse_data(self, filename):
        return Signal(self.read_stripped(filename))

    def part1(self, data) -> int:
        return data.signal_strengths

    def part2(self, data) -> str:
        return data.image


t2 = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

puzzle = Day10()
puzzle.run(13140, t2)
