from itertools import product
import copy

_coords = [(1,  0),  (-1,  0),
            (0,  1),  ( 0, -1),
            (1,  1),  (-1,  1),
            (1, -1),  (-1, -1),]

class World(object):
    def __init__(self, width, height, initial=None):
        self.grid = [[copy.copy(initial) for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def __iter__(self):
        return product(range(self.width), range(self.height))

    def __setitem__(self, coord, it):
        x, y = coord
        self.grid[y][x] = it

    def __getitem__(self, coord):
        x, y = coord
        return self.grid[y][x]

    def copy(self):
        w = World(self.width, self.height)
        w.grid = copy.deepcopy(self.grid)
        return w

    def neighbors(self, x, y):
        indices = [(x + xoff, y + yoff) for xoff, yoff in _coords
                if x + xoff < self.width and y + yoff < self.height
                and x + xoff >= 0 and y + yoff >= 0]

        return [self[x, y] for x, y in indices]

    def __str__(self):
        r = []
        for y in range(self.height):
            l = [str(self[x, y]) for x in range(self.width)]
            r.append("".join(l))
        return "\n".join(r)
