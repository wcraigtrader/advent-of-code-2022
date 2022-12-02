from common import *


def convert_to_int(x): return int(x) if x else None


class Day01(Puzzle):

    def parse_data(self, filename) -> list:
        numbers = map(convert_to_int, self.read_lines(filename))

        snacks = [0]
        for n in numbers:
            if n is None:
                snacks.append(0)
            else:
                snacks[-1] += n

        snacks.sort()

        return snacks

    def part1(self, data) -> int:
        return max(data)

    def part2(self, data) -> int:
        return sum(data[-3:])


puzzle = Day01()
puzzle.run(24000, 45000)
