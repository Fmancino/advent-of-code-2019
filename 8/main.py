#!/usr/bin/env python3
import sys
import copy

def layer_stack(top_layer, bottom_layer):
    result = []
    for t, b in zip(top_layer, bottom_layer):
        if t in (1, 0):
            result.append(t)
        else:
            result.append(b)
    return Layer(result, top_layer.wide, top_layer.tall)

class Layer:

    def __init__(self, numbers, wide, tall):
        self.data = numbers
        self.wide = wide
        self.tall = tall

    def __iter__(self):
        for d in self.data:
            yield d

    def __repr__(self):
        out = ""
        for line in self.as_lines():
            out += f"{line}\n"
        return out

    def as_lines(self):
        start = 0
        yielded_lines = 0
        while yielded_lines != self.tall:
            line = self.data[start:start + self.wide]
            start += self.wide
            yielded_lines += 1
            yield line

    def get_numbers(self):
        l = self.data
        zeroes = [x for x in l if x == 0]
        ones = [x for x in l if x == 1]
        twos = [x for x in l if x == 2]
        return len(zeroes), len(ones), len(twos)

class Picture:

    def __init__(self, inp, wide, tall):
        numbers = []
        self.layers = []
        layer_lenth = wide * tall

        for letter in inp:
            if letter == "\n":
                continue
            numbers.append(int(letter))

        left = len(numbers)
        start = 0
        while left > 0:
            self.layers.append(Layer(numbers[start:start + layer_lenth], wide, tall))
            start += layer_lenth
            left -= layer_lenth

    def __repr__(self):
        out = ""
        for layer in self.layers:
            out += f"{layer}\n"
        return out

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

    def decode(self):
        l = copy.deepcopy(self.layers)
        start = l.pop(0)
        while l != []:
            start = layer_stack(start, l.pop(0))
        return start

def main():
    wide = 25
    tall = 6

    std_in = sys.stdin.read()
    pic = Picture(std_in, wide, tall)
    # Debug
    print(pic)

    # Fist solution
    print("First problem")
    print(pic.get_fist_solution())

    # Second solution
    print("Second problem")
    print(pic.decode())

if __name__ == "__main__":
    main()
