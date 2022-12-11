#! /usr/bin/env python3

import re

from common import *
from dataclasses import dataclass

number = int

@dataclass
class Monkey:
    id: int
    items: list[number]
    operation: str
    operand: number
    divisor: number
    passed: int
    failed: int
    count: int = 0

    def inspect(self, worry: number) -> number:
        if self.operation == 'square':
            new = np.power(worry, 2, dtype=number)
        elif self.operation == 'multiply':
            try:
                new = worry * self.operand
            except FloatingPointError:
                new = int(worry) * int(self.operand)
        elif self.operation == 'add':
            new = worry + self.operand
        return new

    def append(self, item: int) -> None:
        self.items.append(item)

    def clone(self) -> "Monkey":
        items = list(self.items)
        return Monkey(self.id, items, self.operation, self.operand, self.divisor, self.passed, self.failed)

    @property
    def description(self):
        return self.operation if self.operation == 'square' else f'{self.operation} {self.operand}'

    @classmethod
    def parse(cls, lines):
        id = items = operation = operand = divisor = passed = failed = None
        for line in lines:
            tokens = re.split(r'[:, ]+', line)
            match tokens:
                case 'Monkey', value, _:
                    id = int(value)
                case 'Starting', 'items', *values:
                    items = list(map(number, values))
                case 'Operation', 'new', '=', 'old', '*', 'old':
                    operation = 'square'
                case 'Operation', 'new', '=', 'old', '*', value:
                    operation, operand = 'multiply', number(value)
                case 'Operation', 'new', '=', 'old', '+', value:
                    operation, operand = 'add', number(value)
                case 'Test', 'divisible', 'by', value:
                    divisor = number(value)
                case 'If', 'true', 'throw', 'to', 'monkey', value:
                    passed = int(value)
                case 'If', 'false', 'throw', 'to', 'monkey', value:
                    failed = int(value)
                case _:
                    print(f'Did not match {tokens}')

        assert id is not None
        assert items is not None
        assert operation is not None
        assert divisor is not None
        assert passed is not None
        assert failed is not None

        return cls(id, items, operation, operand, divisor, passed, failed)


class Monkeys:

    def __init__(self, lines):
        self.initial = [Monkey.parse(lines[m:m + 6]) for m in range(0, len(lines), 7)]
        self.modulo = number(1)
        for monkey in self.initial:
            self.modulo *= monkey.divisor

    def initialize(self):
        self.monkeys = [monkey.clone() for monkey in self.initial]

    def inspect(self, monkey: Monkey, worry: number) -> number:
        if monkey.operation == 'square':
            new = worry * worry
        elif monkey.operation == 'multiply':
            new = worry * monkey.operand
        elif monkey.operation == 'add':
            new = worry + monkey.operand
        return new % self.modulo

    def round_with_relief(self, relief=None):
        for monkey in self.monkeys:
            monkey.count += len(monkey.items)
            for worry in monkey.items:
                worry = number(self.inspect(monkey, worry)/relief)
                destination = monkey.passed if worry % monkey.divisor == number(0) else monkey.failed
                self.monkeys[destination].append(worry)
            monkey.items = []

    def round(self):
        for monkey in self.monkeys:
            monkey.count += len(monkey.items)
            for worry in monkey.items:
                worry = self.inspect(monkey, worry)
                destination = monkey.passed if worry % monkey.divisor == number(0) else monkey.failed
                self.monkeys[destination].append(worry)
            monkey.items = []

    def print(self):
        for monkey in self.monkeys:
            print(f'Monkey {monkey.id} inspected items {monkey.count} items.')
        print()

    @property
    def two_most_active(self):
        temp = self.monkeys.copy()
        temp.sort(key=lambda x: x.count, reverse=True)
        return temp[0].count * temp[1].count


class Day11(Puzzle):

    def parse_data(self, filename):
        return Monkeys(self.read_stripped(filename))

    def part1(self, data) -> int:
        data.initialize()
        for round in range(20):
            data.round_with_relief(number(3))
        return data.two_most_active

    def part2(self, data) -> int:
        data.initialize()
        for round in range(10000):
            # if round in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            #     print(f'== After round {round} ==')
            #     data.print()

            data.round()

        # data.print()
        
        return data.two_most_active


puzzle = Day11()
puzzle.run(10605, 2713310158)

