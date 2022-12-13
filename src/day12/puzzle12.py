#! /usr/bin/env python3

from common import *
from dataclasses import dataclass
from functools import cache
from sortedcontainers import SortedDict, SortedList


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

class Map(AstarSearch):

    DIRECTIONS = [Position(-1, 0), Position(0, -1), Position(1, 0), Position(0, 1)]

    def __init__(self, raw: str):
        super().__init__()

        # Parse the Grid
        self.grid = [list(map(lambda x: ord(x) - ord('`'), list(l))) for l in raw.splitlines()]

        # Calculate the grid size
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.count = self.rows * self.cols

        # Find the origin and target positions
        self.origin = self.offset(raw.index('S'))
        self.target = self.offset(raw.index('E'))
        self[self.origin] = 1
        self[self.target] = 27

    def __setitem__(self, pos: Position, value: int) -> None:
        """Set a grid value by position"""
        self.grid[pos.row][pos.col] = value

    def __getitem__(self, pos: Position) -> int:
        """Get a grid value by position"""
        return self.grid[pos.row][pos.col]

    def offset(self, index: int) -> Position:
        row = int(index / (self.cols + 1))
        col = index - row * (self.cols + 1)
        return Position(row, col)

    def valid(self, pos: Position) -> bool:
        return (0 <= pos.row < self.rows) and (0 <= pos.col < self.cols)

    def scalable(self, here: Position, there: Position) -> bool:
        return (self[there] - self[here]) <= 1

    @cache
    def neighbors(self, node: Position) -> list[Position]:
        """Return a list of all of the neighbors of a node"""
        neighbors = []
        for direction in self.DIRECTIONS:
            neighbor = node + direction
            if self.valid(neighbor) and self.scalable(node, neighbor):
                neighbors.append(neighbor)
        return neighbors

    def distance(self, src: Position, dst: Position) -> float:
        """Distance between two nodes"""
        rows = abs(src.row - dst.row)
        cols = abs(src.col - dst.col)
        return rows + cols

    def heuristic(self, node: Position) -> float:
        """Estimate the cost to get to the goal from a node"""
        return self.distance(node, self.target)

    def ground_level_starts(self) -> list[Position]:
        return [Position(r, c)
                for r in range(self.rows)
                for c in range(self.cols)
                if self.grid[r][c] == 1]


class Day12(Puzzle):

    def parse_data(self, filename):
        return Map(self.read_blob(filename))

    def part1(self, map: Map) -> int:
        path = map.traverse(map.origin, map.target)
        return len(path) - 1

    def part2(self, map: Map) -> int:
        shortest = 999_999
        for start in map.ground_level_starts():
            path = map.traverse(start, map.target)
            if path is not None:
                shortest = min(shortest, len(path) - 1)

        return shortest


puzzle = Day12()
puzzle.run(31, 29)
