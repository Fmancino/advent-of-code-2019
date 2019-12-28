#!/usr/bin/env python3

class IntcodeComputer:

    def __init__(self, program, input_val=None):
        self.program = program
        self.input_val = input_val

    def gmv(self, run_mem, immediate_value, is_immediate_mode):
        """
        "Get mode value"
        """
        if is_immediate_mode:
            return immediate_value
        return run_mem[immediate_value]

    def run_2args(self, noun, verb):
        r_mem = {}
        r_mem[1] = noun
        r_mem[2] = verb
        return self.run(r_mem)

    def run(self, initial_running_mem):
        pos = 0
        r_mem = RunningMemory(self.program, initial_running_mem)
        while r_mem[pos] != 99:
            item = r_mem[pos]
            opcode = item % 100
            modes = get_modes(item // 100)

            if opcode == 1:
                pos_n1 = r_mem[pos + 1]
                pos_n2 = r_mem[pos + 2]
                pos_result = r_mem[pos + 3]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                r_mem[pos_result] = val_n1 + val_n2
                pos += 4

            elif opcode == 2:
                pos_n1 = r_mem[pos + 1]
                pos_n2 = r_mem[pos + 2]
                pos_result = r_mem[pos + 3]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                r_mem[pos_result] = val_n1 * val_n2
                pos += 4

            elif opcode == 3: # in
                pos_n1 = r_mem[pos + 1]
                r_mem[pos_n1] = self.input_val
                pos += 2

            elif opcode == 4: # out
                pos_n1 = r_mem[pos + 1]
                out = self.gmv(r_mem, pos_n1, modes[1])
                print(self.gmv(r_mem, pos_n1, modes[1]))
                pos += 2

            elif opcode == 5:  #jump if true
                pos_n1 = r_mem[pos + 1]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                if val_n1 != 0:
                    pos_n2 = r_mem[pos + 2]
                    val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                    pos = val_n2
                else:
                    pos += 3

            elif opcode == 6:  #jump if false
                pos_n1 = r_mem[pos + 1]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                if val_n1 == 0:
                    pos_n2 = r_mem[pos + 2]
                    val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                    pos = val_n2
                else:
                    pos += 3

            elif opcode == 7:  #less than
                pos_n1 = r_mem[pos + 1]
                pos_n2 = r_mem[pos + 2]
                pos_result = r_mem[pos + 3]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                if val_n1 < val_n2:
                    r_mem[pos_result] = 1
                else:
                    r_mem[pos_result] = 0
                pos += 4

            elif opcode == 8:  #equals
                pos_n1 = r_mem[pos + 1]
                pos_n2 = r_mem[pos + 2]
                pos_result = r_mem[pos + 3]
                val_n1 = self.gmv(r_mem, pos_n1, modes[1])
                val_n2 = self.gmv(r_mem, pos_n2, modes[2])
                if val_n1 == val_n2:
                    r_mem[pos_result] = 1
                else:
                    r_mem[pos_result] = 0
                pos += 4

            else:
                raise ValueError(f"unexpected number: {opcode}")
        return r_mem[0]

class RunningMemory:

    def __init__(self, program, initial_run_mem):
        self.program = program
        self.run_mem = initial_run_mem

    def __setitem__(self, key, value):
        self.run_mem[key] = value

    def __getitem__(self, pos):
        """
        "Get run value"
        Optimization step, run_mem is the memory when running the program with
        a certain argument, and to get a value we first check if we have it in
        the running memory, and if not we get it from the "immutable" saved state (self.program)
        """
        try:
            return self.run_mem[pos]
        except KeyError:
            self.run_mem[pos] = self.program[pos]
        return self.run_mem[pos]



def get_modes(modes_int):
    modes = {1: False, 2: False, 3: False}
    modes[3] = (modes_int // 100) == 1
    modes2 = modes_int % 100
    modes[2] = (modes2 // 10) == 1
    modes[1] = (modes2 % 10) == 1
    return modes
