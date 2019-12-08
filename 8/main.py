#!/usr/bin/env python3
import sys
import copy

WIDE = 25
TALL = 6
LAYER = WIDE * TALL

def layer_stack(top_layer, bottom_layer):
    result = []
    for t, b in zip(top_layer, bottom_layer):
        if t in (1, 0):
            result.append(t)
        else:
            result.append(b)
    return Layer(result)

class Layer:

    def __init__(self, numbers):
        self.data = numbers

    def __iter__(self):
        for d in self.data:
            yield d

    def as_lines(self):
        start = 0
        layer = []
        while len(layer) != TALL:
            line = self.data[start:start + WIDE]
            start += WIDE
            layer.append(copy.deepcopy(line))
        return layer

    def pretty_print(self):
        for line in self.as_lines():
            print(line)

    def get_numbers(self):
        l = self.data
        zeroes = [x for x in l if x == 0]
        ones = [x for x in l if x == 1]
        twos = [x for x in l if x == 2]
        return len(zeroes), len(ones), len(twos)

class Picture:

    def __init__(self, inp):
        numbers = []
        self.layers = []

        for letter in inp:
            if letter == "\n":
                continue
            numbers.append(int(letter))

        left = len(numbers)
        start = 0
        while left > 0:
            self.layers.append(Layer(numbers[start:start + LAYER]))
            start += LAYER
            left -= LAYER

    def pretty_print(self):
        for layer in self.layers:
            layer.pretty_print()
            print()


    def get_fist_solution(self):
        best_layer = []
        smallest_length = 999999
        for layer in self.layers:
            num_zero, _, _ = layer.get_numbers()
            if num_zero < smallest_length:
                smallest_length = num_zero
                best_layer = layer
        _, n1, n2 = best_layer.get_numbers()

        return n1 * n2

    def print_final(self):
        start = self.layers.pop(0)
        while self.layers != []:
            start = layer_stack(start, self.layers.pop(0))
        start.pretty_print()



def main():
    std_in = sys.stdin.read()
    pic = Picture(std_in)
    pic.pretty_print()
    print(pic.get_fist_solution())
    pic.print_final()

if __name__ == "__main__":
    main()
