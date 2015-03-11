import pygame
import time
import sys
from pygame import display, draw, event

pygame.init()

surf = display.set_mode((0, 0), pygame.DOUBLEBUF|pygame.HWSURFACE)

from world import World

import conway
import forest_fire

if len(sys.argv) > 1 and sys.argv[1] == "conway":
    update = conway.conway
    Cell = conway.Cell
else:
    update = forest_fire.forest_fire
    Cell = forest_fire.Cell

PIXEL_WIDTH = 100

w = World(surf.get_width() // PIXEL_WIDTH, surf.get_height() // PIXEL_WIDTH, Cell.initial())

pause = False

last_tick = time.time() - 1

while True:
    start = time.time()


    for evt in event.get():
        if evt.type == pygame.QUIT:
            exit()
        elif evt.type == pygame.MOUSEBUTTONDOWN:
            x, y = evt.pos
            x = x // PIXEL_WIDTH
            y = y // PIXEL_WIDTH
            w[x, y].toggle()
            w[x, y].render(x, y, PIXEL_WIDTH, surf)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == 32:
                pause = not pause
            elif evt.key == 27:
                exit()

    if not pause and time.time() - last_tick > 0.250:
        update(w)
        surf.fill((230,255,230), (0, 0, surf.get_width(), surf.get_height()))
        for x, y in w:
            w[x, y].render(x, y, PIXEL_WIDTH, surf)
        last_tick = time.time()

    display.flip()
    ideal = (1.0/60) - time.time() - start
    time.sleep(max(ideal, 0))
