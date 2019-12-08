#!/usr/bin/env python3
import sys
import itertools
import copy

def int_run(program, noun, verb):
    ret = copy.deepcopy(program)
    ret[1] = noun
    ret[2] = verb
    pos = 0
    while ret[pos] != 99:
        item = ret[pos]
        pos_n1 = ret[pos + 1]
        pos_n2 = ret[pos + 2]
        pos_result = ret[pos + 3]
        if item == 1:
            ret[pos_result] = ret[pos_n1] + ret[pos_n2]
        elif item == 2:
            ret[pos_result] = ret[pos_n1] * ret[pos_n2]
        else:
            raise
        pos += 4
    return ret[0]

def try_all_combinations(program, exp_result, max_range):
    for noun in range(max_range):
        for verb in range(max_range):
            res = int_run(program, noun, verb)
            if res == exp_result:
                return noun*100 + verb


def main():
    std_in = sys.stdin.read()
    std_in_numbers = map(int, std_in.split(","))
    prog = dict(zip(itertools.count(), std_in_numbers))

    print("first star")
    print(int_run(prog, 12, 2))
    print("second star")
    print(try_all_combinations(prog, 19690720, 100))



if __name__ == "__main__":
    main()
