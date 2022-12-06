#! /usr/bin/env python3

from common import *
from dataclasses import dataclass


@dataclass
class CleanupRange:
    entry: str

    def __post_init__(self):
        first, _, second = self.entry.partition(',')
        head1, _, tail1 = first.partition('-')
        self.head1, self.tail1 = int(head1), int(tail1)
        head2, _, tail2 = second.partition('-')
        self.head2, self.tail2 = int(head2), int(tail2)

        assert self.head1 <= self.tail1
        assert self.head2 <= self.tail2

    @property
    def wholly_contained(self) -> bool:
        first = self.head1 <= self.head2 <= self.tail2 <= self.tail1
        second = self.head2 <= self.head1 <= self.tail1 <= self.tail2
        return first or second

    @property
    def partial_overlap(self):
        t1 = self.head1 <= self.head2 <= self.tail1
        t2 = self.head2 <= self.head1 <= self.tail2
        t3 = self.head1 <= self.tail2 <= self.tail1
        t4 = self.head2 <= self.tail1 <= self.tail2
        return t1 or t2 or t3 or t4


class Day04(Puzzle):

    def parse_data(self, filename):
        return [CleanupRange(line) for line in self.read_stripped(filename)]

    def part1(self, data) -> int:
        return len(list(filter(lambda x: x.wholly_contained, data)))

    def part2(self, data) -> int:
        return len(list(filter(lambda x: x.partial_overlap, data)))


puzzle = Day04()
puzzle.run(2, 4)
