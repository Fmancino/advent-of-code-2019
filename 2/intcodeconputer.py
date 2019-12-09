#!/usr/bin/env python3

class IntcodeComputer:

    def __init__(self, program):
        self.program = program

    def grv(self, run_mem, pos):
        """
        "Get run value"
        Optimization step, run_mem is the memory when running the program with
        a certain argument, and to get a value we first check if we have it in
        the running memory, and if not we get it from the "immutable" saved state (self.program)
        """
        try:
            return run_mem[pos]
        except KeyError:
            run_mem[pos] = self.program[pos]
        return run_mem[pos]

    def run_2args(self, noun, verb):
        r_mem = {}
        r_mem[1] = noun
        r_mem[2] = verb
        return self.run(r_mem)

    def run(self, r_mem):
        pos = 0
        while self.grv(r_mem, pos) != 99:
            item = self.grv(r_mem, pos)
            pos_n1 = self.grv(r_mem, pos + 1)
            pos_n2 = self.grv(r_mem, pos + 2)
            pos_result = self.grv(r_mem, pos + 3)
            if item == 1:
                r_mem[pos_result] = self.grv(r_mem, pos_n1) + self.grv(r_mem, pos_n2)
            elif item == 2:
                r_mem[pos_result] = self.grv(r_mem, pos_n1) * self.grv(r_mem, pos_n2)
            else:
                raise ValueError(f"unexpected number: {item}")
            pos += 4
        return r_mem[0]
