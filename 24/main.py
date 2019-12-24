#!/usr/bin/env python3
import sys
import copy
import math
from collections import OrderedDict

class Space:

    def __init__(self, text, wide):

        self.no_data = ['.'*5]*5

        self.data = OrderedDict()
        self.data[0] = Tile(text)
        self.tile_size = len(self.data[0])
        self.min_lvl = 0
        self.max_lvl = 1
        self.bug = '#'
        self.empty = '.'

    def __iter__(self):
        for lvl in self.data:
            for place in lvl:
                yield place

    def get_coordinates(self, index):
        tile_index = index % self.tile_size
        z = (index // self.tile_size) + self.min_lvl
        return tile_index, z

    def minute_pass(self):
        original = copy.deepcopy(self)
        for count, place in enumerate (original):
            if place == self.bug and original_tile.bug_dies(count):
                self[count] = self.empty
            if place == self.empty and original_tile.space_is_infested(count):
                self[count] = self.bug
        return original_tile

    def get_num_levels(self):
        return self.max_lvl - selv.min_lvl

    def bug_dies(self, index):
        ti, lvl = self.get_coordinates(index)
        try:
            self.data[lvl]
        except KeyError:
            self.data[lvl] = Tile(self.no_data)
        

        close = self.data[lvl].get_close_coordinates_3d(ti, lvl)
        bug_count = 0
        for x,y,z in close:
            if self.data[lvl].data[y][x] == self.bug:
                bug_count += 1
        if bug_count == 1:
            return False
        else:
            return True

    def minute_pass(self):
        if self.data[self.min_lvl] != Tile(self.no_data):
            self.min_lvl
        original_tile = Tile(self.data)
        for count, place in enumerate (original_tile):
            if place == self.bug and original_tile.bug_dies(count):
                self[count] = self.empty
            if place == self.empty and original_tile.space_is_infested(count):
                self[count] = self.bug
        return original_tile

class Tile:

    def __init__(self, text):
        data_lines = []
        for line in text:
            data_line = []
            for letter in line:
                if letter in "#.":
                    data_line.append(letter)
            data_lines.append(data_line)

        self.wide = len(data_lines)
        self.data = data_lines
        self.middle = self.wide // 2 + self.wide % 2
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

    def get_close_coordinates_3d(self, index, lvl):
        x, y = self.get_coordinates(index)
        res = []
        if x == self.middle and y== self.middle:
            return res []

        if x != 0:
            res += [(x-1, y, lvl)]
        else:
            res += [(self.middle-1, self.middle, lvl+1)]
        if y != 0:
            res += [(x, y-1, lvl)]
        else:
            res += [(self.middle, self.middle-1, lvl+1)]
        if y != self.wide - 1:
            res += [(x, y+1)]
        else:
            res += [(self.middle, self.middle+1, lvl+1)]
        if x != self.wide - 1:
            res += [(x+1, y)]
        else:
            res += [(self.middle+1, self.middle, lvl+1)]

        middle_point = (self.middle, self.middle, lvl)

        if middle_point in res:
            res.remove(middle_point)
            if x == self.middle-1:
                for i in range(self.wide):
                    res += [(0, i, lvl-1)]
            elif x == self.middle+1:
                for i in range(self.wide):
                    res += [(self.wide-1, i, lvl-1)]
            elif y == self.middle+1:
                for i in range(self.wide):
                    res += [(i, self.wide-1, lvl-1)]
            elif y == self.middle-1:
                for i in range(self.wide):
                    res += [(i, 0, lvl-1)]
            else:
                raise ValueError
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

    def __len__(self):
        return self.wide * self.wide

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
        original_tile = Tile(self.data)
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

    std_in = sys.stdin.readlines()
    tile = Tile(std_in)
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
