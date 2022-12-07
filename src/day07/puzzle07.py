#! /usr/bin/env python3

from common import *
from dataclasses import dataclass, field


@dataclass
class Directory:
    parent: "Directory" = None
    contents: dict = field(default_factory=dict)

    @property
    def size(self) -> int:
        size = 0
        for value in self.contents.values():
            size += value.size if isinstance(value, Directory) else value
        return size

    @property
    def subdirectories(self) -> list["Directory"]:
        results = []
        for value in self.contents.values():
            if isinstance(value, Directory):
                results.append(value)
                results.extend(value.subdirectories)
        return results


class Day07(Puzzle):

    def parse_data(self, filename):
        return self.parse_commands(self.read_stripped(filename))

    def parse_commands(self, lines: list[str]) -> Directory:
        result = Directory()

        for line in lines:
            match line.split(' '):
                case "$", "cd", "/":
                    current = result
                case "$", "cd", "..":
                    current = current.parent
                case "$", "cd", directory:
                    current = current.contents[directory]
                case "$", "ls":
                    pass
                case "dir", directory:
                    current.contents[directory] = Directory(current)
                case size, filename:
                    current.contents[filename] = int(size)

        return result

    def part1(self, data: Directory) -> int:
        return sum(d.size for d in data.subdirectories if d.size <= 100000)

    def part2(self, data: Directory) -> int:
        total, required = 70_000_000, 30_000_000
        unused = total - data.size
        needed = required - unused

        candidates = [d for d in data.subdirectories if d.size >= needed]
        candidates.sort(key=lambda x: x.size)

        return candidates[0].size


puzzle = Day07()
puzzle.run(95437, 24933642)
