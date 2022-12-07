import os
import sys
import time


class Puzzle(object):
    """This is a framework for solving each day's puzzle"""

    def __init__(self, datafile: str = 'real.data', testfile: str = 'test.data'):
        self.base = os.path.dirname(sys.argv[0])

        self.datafile = datafile
        self.testfile = testfile

        self.data = None
        self.test = None

        self._started = 0
        self._elapsed = 0

    # ----- Methods each Puzzle needs to implement ----------------------------

    def parse_data(self, filename):
        """Parse a data file, returning data for each part of the puzzle"""
        raise NotImplementedError('parse_data')

    def part1(self, data) -> int:
        """Implement part 1 of the puzzle"""
        raise NotImplementedError('part1')

    def part2(self, data) -> int:
        """Implement part 2 of the puzzle"""
        raise NotImplementedError('part2')

    # ----- Useful methods for parsing data files -----------------------------

    def read_lines(self, filename: str) -> list[str]:
        """Read a data file, returning a list, one entry per line"""

        with open(os.path.join(self.base, filename), 'r') as df:
            return df.readlines()

    def read_stripped(self, filename: str) -> list[str]:
        """Read a data file, stripping leading and trailing white space"""

        return list(map(str.strip, self.read_lines(filename)))

    # ----- Test runner -------------------------------------------------------

    def run(self, test1: int | list = None, test2: int | list = None) -> None:
        """Load data and run tests"""

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

    def single_test(self, name: str, expected):
        """Execute one test run and one real run for part1 or part2"""

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
        """Execute multiple test runs and one real run for part1 or part2"""

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

    # ----- Internal methods --------------------------------------------------

    def start(self):
        """Start a timer"""
        self._started = time.perf_counter_ns()

    def stop(self):
        """Stop the timer and save the elapsed time in milliseconds"""
        self._elapsed = (time.perf_counter_ns() - self._started) / 1_000_000

    @property
    def elapsed(self):
        """Format the elapsed time in milliseconds"""
        return f'{self._elapsed:6.3f} ms'
