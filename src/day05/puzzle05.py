#! /usr/bin/env python3

from dataclasses import dataclass
from collections import OrderedDict

from common import *


@dataclass
class Move:

    qty: int
    src: str
    dst: str

    @classmethod
    def parse(cls, line):
        match line.strip().split(' '):
            case 'move', qty, 'from', src, 'to', dst:
                return cls(int(qty), src, dst)

        raise ValueError(f'Could not parse: {line}')


class Stacks:

    def __init__(self, lines: list[str]):
        self.initial = OrderedDict()

        lines = list(reversed(lines))

        numbers = lines[0].strip().replace(' ', '')
        for number in numbers:
            self.initial[number] = list()

        for level in lines[1:]:
            for stack, pos in enumerate(range(1, len(level), 4), 1):
                crate = level[pos]
                if crate != ' ':
                    self.initial[str(stack)].insert(0, crate)

    def initialize(self):
        self.stacks = OrderedDict()
        for key, value in self.initial.items():
            self.stacks[key] = value.copy()

    def move_9000_crates(self, move: Move) -> None:
        for i in range(move.qty):
            crate = self.stacks[move.src].pop(0)
            self.stacks[move.dst].insert(0, crate)

    def execute_9000(self, moves: list[Move]) -> None:
        self.initialize()
        for move in moves:
            self.move_9000_crates(move)

    def move_9001_crates(self, move: Move) -> None:
        self.stacks[move.dst] = self.stacks[move.src][:move.qty] + self.stacks[move.dst]
        del self.stacks[move.src][:move.qty]

    def execute_9001(self, moves: list[Move]) -> None:
        self.initialize()
        for move in moves:
            self.move_9001_crates(move)

    @property
    def top_crate_names(self) -> str:
        return ''.join(stack[0] for stack in self.stacks.values())


@dataclass
class Orders:

    stacks: Stacks
    moves: list[Move]

    def part1(self) -> str:
        self.stacks.execute_9000(self.moves)
        return self.stacks.top_crate_names

    def part2(self) -> str:
        self.stacks.execute_9001(self.moves)
        return self.stacks.top_crate_names


class Day05(Puzzle):

    def parse_data(self, filename):
        lines = self.read_lines(filename)
        blank_line = lines.index('\n')

        stacks = Stacks(lines[:blank_line])
        moves = [Move.parse(line) for line in lines[blank_line + 1:]]
        return Orders(stacks, moves)

    def part1(self, orders: Orders) -> str:
        return orders.part1()

    def part2(self, orders: Orders) -> str:
        return orders.part2()


puzzle = Day05()
puzzle.run('CMZ', 'MCD')
