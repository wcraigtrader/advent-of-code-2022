#! /usr/bin/env python3

from dataclasses import dataclass

from common import *


@dataclass
class RuckSack:

    contents: str

    @property
    def common_items(self):
        self.count = len(self.contents)
        assert self.count % 2 == 0, f'{self.count} items in {self.contents}'

        half = int(self.count / 2)
        self.compartment1 = self.contents[:half]
        self.compartment2 = self.contents[half:]
        assert len(self.compartment1) == len(self.compartment2)

        self.set1 = set(self.compartment1)
        self.set2 = set(self.compartment2)

        return list(self.set1 & self.set2)

    @property
    def total_common_priorities(self):
        return sum(list(map(self.priority, self.common_items)))

    @staticmethod
    def priority(item: str) -> int:
        order = ord(item)
        if ord('a') <= order and order <= ord('z'):
            return order - ord('a') + 1
        if ord('A') <= order and order <= ord('Z'):
            return order - ord('A') + 27

        raise ValueError(f'Unexpected {item}')


class Day03(Puzzle):

    def parse_data(self, filename):
        return list(map(RuckSack, self.read_stripped(filename)))

    def part1(self, data) -> int:
        return sum(sack.total_common_priorities for sack in data)

    def part2(self, data) -> int:
        result = 0

        for sacks in [data[i:i + 3] for i in range(0, len(data), 3)]:
            for badge in set(sacks[0].contents) & set(sacks[1].contents) & set(sacks[2].contents):
                result += RuckSack.priority(badge)

        return result


puzzle = Day03()
puzzle.run(157, 70)
