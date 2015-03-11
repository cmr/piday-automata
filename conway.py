from world import World

from pygame import draw

class Cell(object):
    def __init__(self, state):
        self.state = state

    @classmethod
    def initial(cls):
        return Cell(0)

    def is_alive(self):
        return self.state == 1

    def render(self, x, y, width, surf):
        col = (0,0,0)

        if self.state == 1:
            col = (255, 255, 255)

        surf.fill(col, (x*width, y*width, width, width))

    def toggle(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

def conway(world):
    w = world.copy()
    for x, y in w:
        live = len(filter(Cell.is_alive, w.neighbors(x, y)))
        if live < 2:
            # die of under-population
            world[x, y] = Cell(0)
        elif live == 2:
            # no change
            pass
        elif live == 3:
            # reproduce
            world[x, y] = Cell(1)
        else:
            # die of overcrowding
            world[x, y] = Cell(0)
