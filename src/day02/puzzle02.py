#! /usr/bin/env python3

from dataclasses import dataclass

from common import *

DECODE = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}

WIN = [None, 2, 3, 1]
DRAW = [None, 1, 2, 3]
LOSE = [None, 3, 1, 2]
RULE = [None, LOSE, DRAW, WIN]


@dataclass
class Advice:
    opponent: str
    advice: str

    @property
    def score1(self) -> int:
        opponent, response = DECODE[self.opponent], DECODE[self.advice]
        score = response + self.outcome(opponent, response)
        return score

    @property
    def score2(self) -> int:
        opponent, goal = DECODE[self.opponent], DECODE[self.advice]
        response = RULE[goal][opponent]
        score = response + self.outcome(opponent, response)
        return score

    @staticmethod
    def outcome(opponent: int, response: int) -> int:
        outcome = ((response - opponent + 1) % 3) * 3
        return outcome

    @classmethod
    def parse(cls, line: str) -> "Advice":
        opponent, advice = line.split(' ')
        return cls(opponent, advice)

class Day02(Puzzle):

    def parse_data(self, filename):
        return list(map(Advice.parse, self.read_stripped(filename)))

    def part1(self, data) -> int:
        return sum(match.score1 for match in data)

    def part2(self, data) -> int:
        return sum(match.score2 for match in data)


puzzle = Day02()
puzzle.run(15, 12)
