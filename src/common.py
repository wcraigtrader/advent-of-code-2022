import os
import sys
import time


class Puzzle(object):
    """This is a framework for solving each day's puzzle"""

    def __init__(self, datafile: str = 'real.data', *testfiles: str):
        self.base = os.path.dirname(sys.argv[0])

        self.datafile = datafile
        self.testfiles = testfiles

        if len(testfiles) == 0:
            self.testfiles = [ 'test.data' ]

        self.data = None
        self.tests = None

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

        self.tests = [self.parse_data(tf) for tf in self.testfiles]
        self.data = self.parse_data(self.datafile)

        if test1 is not None:
            if isinstance(test1, list):
                if len(self.tests) == len(test1):
                    self.multi_test('part1', test1, self.tests, True)
                else:
                    self.multi_test('part1', test1, self.tests[0], False)
            else:
                self.single_test('part1', test1)

        if test2 is not None:
            if isinstance(test2, list):
                if len(self.tests) == len(test2):
                    self.multi_test('part2', test2, self.tests, True)
                else:
                    self.multi_test('part2', test2, self.tests[0], False)
            else:
                self.single_test('part2', test2)

    def single_test(self, name: str, expected):
        """Execute one test run and one real run for part1 or part2"""

        method = getattr(self, name)

        self.start()
        test_result = method(self.tests[0])
        self.stop()
        print(f'{self.elapsed}: {name} test = {test_result}')
        assert test_result == expected, f'Was {test_result}, should have been {expected}'

        self.start()
        real_result = method(self.data)
        self.stop()
        print(f'{self.elapsed}: {name} real = {real_result}')

    def multi_test(self, name: str, expectations: list, testdata: list, multifile: bool):
        """Execute multiple test runs and one real run for part1 or part2"""

        method = getattr(self, name)

        for i, (test, expected) in enumerate(zip(testdata, expectations), 1):
            self.start()
            result = method(test)
            self.stop()
            passed = 'passed' if result == expected else 'failed'
            print(f'{self.elapsed}: {name} test {i}, {expected} == {result} => {passed}')

        self.start()
        real_result = method(self.data) if multifile else method(self.data[0])
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
