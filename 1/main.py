#!/usr/bin/env python3
import sys

def get_fuel(f):
    return int(f) // 3 - 2

def get_mod_fuel(mod):
    res = get_fuel(mod)
    if res <= 0:
        return 0
    return res + get_mod_fuel(res)

def main():
    std_in = sys.stdin.readlines()

    tot1 = sum(map(get_fuel, std_in))
    print(f"part 1: {tot1}")

    tot2 = sum(map(get_mod_fuel, std_in))
    print(f"part 2: {tot2}")

if __name__ == "__main__":
    main()
