#!/usr/bin/env python3
import sys
import copy
import math
from collections import OrderedDict

class Space:

    def __init__(self, tiles):

        self.no_data = ['.'*5]*5
        self.no_tile = Tile(self.no_data)

        self.data = tiles
        self.tile_size = len(self.data[0])
        self.min_lvl = 0
        self.max_lvl = 1
        self.bug = '#'
        self.empty = '.'

    def __iter__(self):
        for key in self.data:
            for place in key:
                yield place

    def __repr__(self):
        out = ""
        for lvl_key in self.data:
            #  out += f"level {lvl_key}\n"
            out += f"{lvl_key}"
            out += "\n"
        return out

    def get_coordinates(self, index):
        tile_index = index % self.tile_size
        z = (index // self.tile_size)
        return tile_index, z

    def bug_dies(self, index):
        ti, lvl = self.get_coordinates(index)
        close = self.data[lvl].get_close_coordinates_3d(ti, lvl)

        if self.count_bugs(close) == 1:
            return False
        return True

    def count_bugs(self, close_places):
        bug_count = 0
        for x,y,z in close_places:
            try:
                if self.data[z].data[y][x] == self.bug:
                    bug_count += 1
            except IndexError:
                # if the level does no exist it is empty at this point
                continue
        return bug_count

    def get_all_bugs(self):
        bug_count = 0
        for place in self:
            if place == self.bug:
                bug_count += 1
        return bug_count

    def space_is_infested(self, index):
        ti, lvl = self.get_coordinates(index)
        close = self.data[lvl].get_close_coordinates_3d(ti, lvl)

        if self.count_bugs(close) in [1,2]:
            return True
        return False

    def minute_pass(self):
        if self.data[0] != self.no_tile:
            self.data.insert(0, Tile(self.no_data))
        if self.data[len(self.data)-1] != self.no_tile:
            self.data.append(Tile(self.no_data))

        original_space = copy.deepcopy(self)
        for count, place in enumerate (original_space):
            if place == self.bug and original_space.bug_dies(count):
                self[count] = self.empty
            if place == self.empty and original_space.space_is_infested(count):
                self[count] = self.bug

    def __setitem__(self, key, value):
        ti, lvl = self.get_coordinates(key)
        self.data[lvl][ti] = value

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
        self.middle = self.wide // 2
        self.bug = '#'
        self.empty = '.'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        # the constructor does a copy of input, so deepcopy does not need to deepcopy input
        return type(self)(self.data)

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
        if x == self.middle and y == self.middle:
            return res

        if x != 0:
            res += [(x-1, y, lvl)]
        else:
            res += [(self.middle-1, self.middle, lvl+1)]
        if y != 0:
            res += [(x, y-1, lvl)]
        else:
            res += [(self.middle, self.middle-1, lvl+1)]
        if y != self.wide - 1:
            res += [(x, y+1, lvl)]
        else:
            res += [(self.middle, self.middle+1, lvl+1)]
        if x != self.wide - 1:
            res += [(x+1, y, lvl)]
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
    print("First star:")
    # print(tile)
    print(tile.get_biodiversity_rating())
    print("Second star:")
    minutes = 0
    space = Space([Tile(std_in)])
    bugs = space.get_all_bugs()
    while minutes != 200:
        space.minute_pass()
        minutes += 1
    bugs = space.get_all_bugs()
    # print(space)
    print(f"minutes: {minutes}")
    print(f"populated levels: {len(space.data)-2}")
    print(f"bugs: {bugs}")

def tile_in_history(tile, history):
    for t in history:
        if tile.data == t.data:
            return True
    return False


if __name__ == "__main__":
    main()
