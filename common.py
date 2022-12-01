import os


def set_directory(filename):
    os.chdir(os.path.dirname(filename))


class Puzzle(object):

    def __init__(self, datafile: str = 'puzzle.data', testfile: str = 'puzzle.test'):
        self.datafile = datafile
        self.testfile = testfile
        self.data = []
        self.test = []

    def parse_data(self, filename):
        return self.read_data(filename)

    def read_data(self, filename: str) -> list[str]:
        with open(filename, 'r') as df:
            return [l.strip() for l in df.readlines()]

    def part1(self, data: list) -> int:
        raise NotImplementedError('part1')

    def part2(self, data: list) -> int:
        raise NotImplementedError('part2')

    def run(self, test1: int = None, test2: int = None) -> None:

        self.test = self.parse_data(self.testfile)
        self.data = self.parse_data(self.datafile)

        if test1 is not None:
            test_result = self.part1(self.test)
            print( f'part1 test = {test_result}')
            assert test_result == test1
            real_result = self.part1(self.data)
            print( f'part1 real = {real_result}')

        if test2 is not None:
            test_result = self.part2(self.test)
            print( f'part2 test = {test_result}')
            assert test_result == test2
            real_result = self.part2(self.data)
            print( f'part2 real = {real_result}')


set_directory(__file__)
