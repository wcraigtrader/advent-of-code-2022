#! /usr/bin/env python3

from common import *
from enum import Enum


Tile = Enum('Tile', 'Air Rock Sand')


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

    @classmethod
    def parse(cls, pair: str) -> 'Position':
        col, row = map(int, pair.split(','))
        return cls(row, col)


class Cave:

    DOWN = Position(1, 0)
    LEFT = Position(1, -1)
    RIGHT = Position(1, 1)

    def __init__(self, walls: list[str]):
        self.DIRECTIONS = [self.DOWN, self.LEFT, self.RIGHT]

        self.space: dict(Position, Tile) = {}
        self.origin = Position(0, 500)
        self.walls = walls

    def __setitem__(self, pos: Position, value: Tile) -> None:
        """Set a space value by position"""
        self.space[pos] = value
        self.expand_bounds(pos)

    def __getitem__(self, pos: Position) -> Tile:
        """Get a space value by position
        
        If the value isn't set, set it to Air,
        Unless there's a floor and it's at floor-level, in which case return Rock.
        """
        if pos not in self.space:
            if self.floor and pos.row >= self.max_row + 2:
                return Tile.Rock

            self.expand_bounds(pos)
            self[pos] = Tile.Air
        return self.space[pos]

    def expand_bounds(self, pos: Position) -> None:
        if self.expanding:
            self.min_row = min(self.min_row, pos.row)
            self.max_row = max(self.max_row, pos.row)
            self.min_col = min(self.min_col, pos.col)
            self.max_col = max(self.max_col, pos.col)


    def mark_walls(self, floor: bool) -> None:
        self.space = {}
        self.floor = floor

        self.min_row = self.max_row = 0
        self.min_col = self.max_col = 500

        self.expanding = True

        for wall in self.walls:
            corners = list(map(Position.parse, wall.split(' -> ')))
            for i in range(len(corners) - 1):
                c1, c2 = corners[i:i + 2]
                if c1.row == c2.row:
                    row = c1.row
                    if c1.col < c2.col:  # rock right
                        for col in range(c1.col, c2.col + 1, 1):
                            self[Position(row, col)] = Tile.Rock
                    elif c1.col > c2.col:  # rock left
                        for col in range(c1.col, c2.col - 1, -1):
                            self[Position(row, col)] = Tile.Rock
                elif c1.col == c2.col:
                    col = c1.col
                    if c1.row < c2.row:  # rock down
                        for row in range(c1.row, c2.row + 1, 1):
                            self[Position(row, col)] = Tile.Rock
                    elif c1.row > c2.row:  # rock up
                        for row in range(c1.row, c2.row - 1, -1):
                            self[Position(row, col)] = Tile.Rock

        self.expanding = False

    def in_bounds(self, pos: Position) -> bool:
        return (self.min_row <= pos.row <= self.max_row) and (self.min_col <= pos.col <= self.max_col)

    def fall(self, pos: Position) -> Position:
        for direction in self.DIRECTIONS:
            next=pos + direction
            if self[next] == Tile.Air:
                return next
        return None

    def fill_with_sand(self, floor: bool) -> int:

        self.mark_walls(floor)

        sand_count = 0

        filling = True
        while filling:
            falling = True
            pos = self.origin
            while falling: # While a unit of sand is falling
                next = self.fall(pos)

                # If we're blocked below, fill this spot with sand
                if next is None: 
                    self[pos] = Tile.Sand
                    sand_count += 1
                    falling = False

                    # If there's a floor and we've backed up to the top, quit
                    if floor and pos == self.origin:
                        filling = False

                # If there isn't a floor, but we're falling to a bottomless pit, quit
                elif not floor and not self.in_bounds(next):
                    falling, filling = False, False

                # Else, fall some more
                else:
                    pos = next

        return sand_count


class Day14(Puzzle):

    def parse_data(self, filename) -> Cave:
        return Cave(self.read_stripped(filename))

    def part1(self, cave) -> int:
        return cave.fill_with_sand(False)

    def part2(self, cave) -> int:
        return cave.fill_with_sand(True)


puzzle=Day14()
puzzle.run(24, 93)
