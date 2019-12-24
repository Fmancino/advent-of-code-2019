#!/usr/bin/env python3
import sys
import copy
import math

class Tile:

    def __init__(self, text, wide):
        data_lines = []
        for line in text:
            data_line = []
            for letter in line:
                if letter in "#.":
                    data_line.append(letter)
            data_lines.append(data_line)

        self.wide = 5
        self.data = data_lines
        self.bug = '#'
        self.empty = '.'

    def get_coordinates(self, index):
        x = index % self.wide
        y = index // self.wide
        return x,y

    def get_close_coordinates(self, index):
        x, y = self.get_coordinates(index)
        res = []
        if x != 0:
            res += [(x-1, y)]
        if y != 0:
            res += [(x, y-1)]
        if y != self.wide - 1:
            res += [(x, y+1)]
        if x != self.wide - 1:
            res += [(x+1, y)]

        return res

    def bug_dies(self, index):
        close = self.get_close_coordinates(index)
        bug_count = 0
        for x,y in close:
            if self.data[y][x] == self.bug:
                bug_count += 1
        if bug_count == 1:
            return False
        else:
            return True

    def space_is_infested(self, index):
        close = self.get_close_coordinates(index)
        bug_count = 0
        for x,y in close:
            if self.data[y][x] == self.bug:
                bug_count += 1
        if bug_count in [1,2]:
            return True
        else:
            return False



    def __iter__(self):
        for line in self.data:
            for place in line:
                yield place

    def __repr__(self):
        out = ""
        for line in self.data:
            for letter in line:
                out += letter
            out += "\n"
        return out

    def __getitem__(self, key):
        x, y = self.get_coordinates(key)
        return self.data[y][x]

    def __setitem__(self, key, value):
        x, y = self.get_coordinates(key)
        self.data[y][x] = value

    def minute_pass(self):
        original_tile = Tile(self.data, self.wide)
        for count, place in enumerate (original_tile):
            if place == self.bug and original_tile.bug_dies(count):
                self[count] = self.empty
            if place == self.empty and original_tile.space_is_infested(count):
                self[count] = self.bug
        return original_tile

    def get_biodiversity_rating(self):
        bio = 0
        for count, place in enumerate (self):

            if place == self.bug:
                bio += math.pow(2, count)
        return bio



def main():
    wide = 5

    std_in = sys.stdin.readlines()
    tile = Tile(std_in, wide)
    tile_history = []

    while not tile_in_history(tile, tile_history):
        tile_history.append(tile.minute_pass())
    # Debug
    print(tile)
    print(tile.get_biodiversity_rating())

def tile_in_history(tile, history):
    for t in history:
        if tile.data == t.data:
            return True
    return False


if __name__ == "__main__":
    main()
