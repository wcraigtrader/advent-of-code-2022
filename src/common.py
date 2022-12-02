import os
import sys


class Puzzle(object):

    def __init__(self, datafile: str = 'puzzle.data', testfile: str = 'puzzle.test'):
        self.base = os.path.dirname(sys.argv[0])

        self.datafile = datafile
        self.testfile = testfile

        self.data = None
        self.test = None

    def read_lines(self, filename: str) -> list[str]:
        with open(os.path.join(self.base, filename), 'r') as df:
            return [l.strip() for l in df.readlines()]

    def parse_data(self, filename):
        raise NotImplementedError('parse_data')

    def part1(self, data) -> int:
        raise NotImplementedError('part1')

    def part2(self, data) -> int:
        raise NotImplementedError('part2')

    def run(self, test1: int = None, test2: int = None) -> None:

        self.test = self.parse_data(self.testfile)
        self.data = self.parse_data(self.datafile)

        if test1 is not None:
            test_result = self.part1(self.test)
            print( f'part1 test = {test_result}')
            assert test_result == test1, f'Was {test_result}, should have been {test1}'
            real_result = self.part1(self.data)
            print( f'part1 real = {real_result}')

        if test2 is not None:
            test_result = self.part2(self.test)
            print( f'part2 test = {test_result}')
            assert test_result == test2, f'Was {test_result}, should have been {test2}'
            real_result = self.part2(self.data)
            print( f'part2 real = {real_result}')
