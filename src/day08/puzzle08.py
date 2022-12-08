#! /usr/bin/env python3

from common import *
from functools import cache


class Grid:

    def __init__(self, lines):
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.trees = [list(l) for l in lines]

    @cache
    def row(self, row):
        return self.trees[row]

    @cache
    def col(self, col):
        return [self.trees[row][col] for row in range(self.rows)]

    def visible(self, r, c):
        height = self.trees[r][c]
        row = self.row(r)
        col = self.col(c)
        highest = [max(row[:c]), max(row[c + 1:]), max(col[:r]), max(col[r + 1:])]
        visible = height > min(highest)
        return visible

    def scenic(self, r, c):
        height = self.trees[r][c]
        row = self.row(r)
        col = self.col(c)
        up = list(reversed(col[:r]))
        down = col[r + 1:]
        left = list(reversed(row[:c]))
        right = row[c + 1:]

        score = 1
        for sight in (up, down, left, right):
            if not len(sight):
                return 0

            for distance, tree in enumerate(sight, 1):
                if tree >= height:
                    score *= distance
                    break
            else:
                score *= distance

        return score

    @property
    def total_visible(self):
        visible = 2 * self.rows + 2 * self.cols - 4
        visible += sum(1 if self.visible(r, c) else 0
                       for r in range(1, self.rows - 1)
                       for c in range(1, self.cols - 1))
        return visible

    @property
    def most_scenic(self):
        return max(self.scenic(r, c)
                   for r in range(1, self.rows - 1)
                   for c in range(1, self.cols - 1))


class Day08(Puzzle):

    def parse_data(self, filename):
        return Grid(self.read_stripped(filename))

    def part1(self, data) -> int:
        return data.total_visible

    def part2(self, data) -> int:
        return data.most_scenic


puzzle = Day08()
puzzle.run(21, 8)
