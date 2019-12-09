#!/usr/bin/env python3
import sys
import itertools
sys.path.append('../utils')
from intcodeconputer import IntcodeComputer

def try_all_combinations(program, exp_result, max_range):
    for noun in range(max_range):
        for verb in range(max_range):
            res = program.run_2args(noun, verb)
            if res == exp_result:
                return noun*100 + verb
    return None


def main():
    std_in = sys.stdin.read()
    std_in_numbers = map(int, std_in.split(","))
    prog = dict(zip(itertools.count(), std_in_numbers))
    comp = IntcodeComputer(prog)

    print("first star")
    print(comp.run_2args(12, 2))
    print("second star")
    print(try_all_combinations(comp, 19690720, 100))

if __name__ == "__main__":
    main()
