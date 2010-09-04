from __future__ import division
from random import random, randint
# Lets draw a grid of colored quads to represent a grassy field.  Lets render it again as black lines so it looks like a grid.
GRASS = 0
BUNNY = 1

tile_size = 19
gutter_size = 1
width = height = 25
board = [[GRASS for _ in xrange(width)] for _ in xrange(height)]
bunnies = [(5,7),(6,9)]

import pyglet
from pyglet.gl import *

window = pyglet.window.Window()
label = pyglet.text.Label("hello")

#square = pyglet.graphics.vertex_list(

def draw_square(prim=GL_QUADS):
        pyglet.graphics.draw(4, prim,
        ('v2i', (0, 0, 
                 1, 0,
                 1, 1,
                 0, 1))
        )

def draw_board(prim=GL_QUADS):
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            glPushMatrix()

            if (x,y) in bunnies:
                glColor3f(1.0,0,0)
            else:
                glColor3f(0,1.0,0)

            glScalef(tile_size,tile_size,tile_size)
            glTranslatef(x,y,0)
            glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
            draw_square(prim)
            glPopMatrix()



def move_bunny(dt):
    chance_to_move = 0.6
    for index, bunny in enumerate(bunnies):
        if random() > chance_to_move:
            x = randint(-1,1)
            y = randint(-1,1)
            bunnies[index] = (x + bunny[0], y + bunny[1])




pyglet.clock.schedule_interval(move_bunny, 0.1)

@window.event
def on_draw():
        window.clear()
        draw_board()

pyglet.app.run()
