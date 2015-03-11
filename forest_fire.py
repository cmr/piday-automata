from world import World

from pygame import draw, image, transform
import random


burnt_out = image.load("burnt_out.png").convert_alpha()
tree = image.load("tree.png").convert_alpha()

anims = []
growing_anims = []
cur_width = 0

for i in range(10):
    anims.append(image.load("fire{}.png".format(i)).convert_alpha())
    growing_anims.append(image.load("growth{}.png".format(i)).convert_alpha())

class Cell(object):
    def __init__(self):
        self.is_on_fire = False
        self.is_growing = False
        self.burnt_out = False
        self.fully_grown = False
        self.flame_frame = 0
        self.growth_frame = 0

    @classmethod
    def initial(cls):
        return Cell()

    def on_fire(self):
        return self.is_on_fire

    def growing(self):
        return self.is_growing

    def is_fully_grown(self):
        return self.fully_grown

    def render(self, x, y, width, surf):
        # resize sprite if necessary
        global cur_width, burnt_out, tree, anims, growing_anims
        if width != cur_width:
            burnt_out = transform.scale(burnt_out, (width, width))
            tree = transform.scale(tree, (width, width))
            cur_width = width
            anims = [transform.scale(a, (width, width)) for a in anims]
            growing_anims = [transform.scale(a, (width, width)) for a in growing_anims]

        coord = (x*width, y*width, width, width)
        img = None

        if self.is_growing:
            img = growing_anims[self.growth_frame]
        elif self.fully_grown:
            img = tree
        elif self.burnt_out:
            img = burnt_out

        if img is not None:
            surf.blit(img, coord)

        if self.is_on_fire:
            surf.blit(anims[self.flame_frame], coord)

    def toggle(self):
        if self.fully_grown or self.is_growing and not self.burnt_out:
            self.is_on_fire = not self.is_on_fire

        self.flame_frame = 0

def forest_fire(world):
    w = world.copy()

    for x, y in world:
        c = world[x, y]
        neighs = w.neighbors(x, y)
        # if we're on fire, then with very high probability we'll use up some
        # of our fuel
        if c.is_on_fire and random.random() < 0.90:
            c.flame_frame += 1
            # we ran out of fuel!
            if c.flame_frame >= 10:
                c.is_on_fire = False
                c.is_growing = False
                c.fully_grown = False
                c.burnt_out = True

        # if we're still a sapling, then with probability 1/2 we'll grow by
        # one step
        if not c.fully_grown and not c.is_on_fire and not c.burnt_out and random.random() < 0.05:
            c.is_growing = True
            c.growth_frame += 1
            # all grown up!
            if c.growth_frame >= 10:
                c.fully_grown = True
                c.is_growing = False

        if not c.is_on_fire and not c.burnt_out and c.fully_grown or c.is_growing:
            # we catch on fire with a probability based on how many of our
            # neighbors are on fire right now.
            if random.random() < (0.023 * len(filter(Cell.on_fire, neighs))) + 0.000001:
                c.is_on_fire = True
                c.flame_frame = 0

        world[x, y] = c

        if c.burnt_out and len(filter(Cell.on_fire, neighs)) == 0 and random.random() < 0.001:
            world[x, y] = Cell.initial()
