#! /usr/bin/env python3

from common import *
from dataclasses import dataclass


@dataclass
class Move:
    direction: str
    length: int

    @classmethod
    def parse(cls, line):
        direction, length = line.split(' ')
        return cls(direction, int(length))


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, direction: str) -> 'Position':
        match direction:
            case 'R':
                return Position(self.x + 1, self.y)
            case 'L':
                return Position(self.x - 1, self.y)
            case 'U':
                return Position(self.x, self.y + 1)
            case 'D':
                return Position(self.x, self.y - 1)
        raise ValueError(f'Cannot add {direction}')

    def __sub__(self, other: 'Position') -> 'Position':
        return Position(self.x - other.x, self.y - other.y)

    def __rshift__(self, goal: 'Position') -> 'Position':
        offset = goal - self

        if self._touching(goal):
            result = self

        elif offset.x == 0 and offset.y < -1:
            result = Position(self.x, self.y - 1)
        elif offset.x == 0 and offset.y > 1:
            result = Position(self.x, self.y + 1)
        elif offset.x < -1 and offset.y == 0:
            result = Position(self.x - 1, self.y)
        elif offset.x > 1 and offset.y == 0:
            result = Position(self.x + 1, self.y)

        elif offset.x <= -1 and offset.y <= -1:
            result = Position(self.x - 1, self.y - 1)
        elif offset.x <= -1 and offset.y >= 1:
            result = Position(self.x - 1, self.y + 1)
        elif offset.x >= 1 and offset.y <= -1:
            result = Position(self.x + 1, self.y - 1)
        elif offset.x >= 1 and offset.y >= 1:
            result = Position(self.x + 1, self.y + 1)

        else:
            result = self

        return result

    def _touching(self, other: 'Position') -> bool:
        return abs(other.x-self.x) <= 1 and abs(other.y-self.y) <= 1


class Rope:

    def __init__(self, moves: list[Move]):
        self.moves = moves
        self.positions: list[Position] = None
        self.track: set[Position] = None

    def twist(self, length):
        self.positions = [Position(0,0)] * length
        self.track = set()

        head = 0
        tail = -1

        for move in self.moves:
            for step in range(move.length):
                self.positions[head] = self.positions[head] + move.direction
                for knot in range(1, length):
                    self.positions[knot] = self.positions[knot] >> self.positions[knot-1]
                self.track.add(self.positions[tail])

    def print(self, positions, mark=None):
        xl = min(0, min(p.x for p in positions))
        xr = max(0, max(p.x for p in positions))
        xs = xr-xl+1
        xo = -xl

        yd = min(0, min(p.y for p in positions))
        yu = max(0, max(p.y for p in positions))
        ys = yu-yd+1
        yo = -yd

        grid = []
        for y in range(ys):
            grid.append(list('.'*xs))

        for p in range(len(positions)-1,-1,-1):
            pos = positions[p]
            grid[pos.y+yo][pos.x+xo] = mark if mark else 'H' if p == 0 else str(p)

        grid[yo][xo] = 's'

        for line in reversed(grid):
            print(''.join(line))
        print()


class Day09(Puzzle):

    def parse_data(self, filename):
        moves = [Move.parse(line) for line in self.read_stripped(filename)]
        return Rope(moves)

    def part1(self, data) -> int:
        data.twist(2)
        return len(data.track)

    def part2(self, data) -> int:
        data.twist(10)
        return len(data.track)


puzzle = Day09('real.data', 'test1.data', 'test2.data')
puzzle.run(13, [1, 36])
