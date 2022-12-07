import os
import sys
import time


class Puzzle(object):

    def __init__(self, datafile: str = 'real.data', testfile: str = 'test.data'):
        self.base = os.path.dirname(sys.argv[0])

        self.datafile = datafile
        self.testfile = testfile

        self.data = None
        self.test = None

        self._started = 0
        self._elapsed = 0

    def start(self):
        self._started = time.perf_counter_ns()

    def stop(self):
        self._elapsed = (time.perf_counter_ns() - self._started) / 1_000_000

    @property
    def elapsed(self):
        return f'{self._elapsed:6.3f}s'

    def read_lines(self, filename: str) -> list[str]:
        with open(os.path.join(self.base, filename), 'r') as df:
            return df.readlines()

    def read_stripped(self, filename: str) -> list[str]:
        return list(map(str.strip, self.read_lines(filename)))

    def parse_data(self, filename):
        raise NotImplementedError('parse_data')

    def part1(self, data) -> int:
        raise NotImplementedError('part1')

    def part2(self, data) -> int:
        raise NotImplementedError('part2')

    def single_test(self, name: str, expected):
        method = getattr(self, name)

        self.start()
        test_result = method(self.test)
        self.stop()
        print(f'{self.elapsed}: {name} test = {test_result}')
        assert test_result == expected, f'Was {test_result}, should have been {expected}'

        self.start()
        real_result = method(self.data)
        self.stop()
        print(f'{self.elapsed}: {name} real = {real_result}')

    def multi_test(self, name: str, expectations: list):
        method = getattr(self, name)

        for i, (test, expected) in enumerate(zip(self.test, expectations), 1):
            self.start()
            result = method(test)
            self.stop()
            passed = 'passed' if result == expected else 'failed'
            print(f'{self.elapsed}: {name} test {i}, {expected} == {result} => {passed}')

        self.start()
        real_result = method(self.data[0])
        self.stop()
        print(f'{self.elapsed}: {name} real = {real_result}')

    def run(self, test1: int | list = None, test2: int | list = None) -> None:
        self.test = self.parse_data(self.testfile)
        self.data = self.parse_data(self.datafile)

        if test1 is not None:
            if isinstance(test1, list) and len(test1) == len(self.test):
                self.multi_test('part1', test1)
            else:
                self.single_test('part1', test1)

        if test2 is not None:
            if isinstance(test2, list) and len(test2) == len(self.test):
                self.multi_test('part2', test2)
            else:
                self.single_test('part2', test2)
