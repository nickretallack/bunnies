from __future__ import division
from vector import Vector
from glhelper import *

width = height = 25

class World(object):
    def __init__(self, size, bunnies=[]):
        self.grid = [[Cell(Vector(x,y)) for x in xrange(int(size.x))] 
                                        for y in xrange(int(size.y))]
        self.bunnies = bunnies

    def simulate(self, dt):
        for bunny in self.bunnies:
            bunny.simulate(dt)

    def draw(self):
        # TODO: make a better enumerator here.  Use junked walk2d
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                with matrix():
                    glColor3f(0,1.0,0)
                    glScalef(tile_size,tile_size,tile_size)
                    glTranslatef(x, y, 0)
                    glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
                    draw_square(GL_QUADS)

        for bunny in self.bunnies:
            bunny.draw()

class Cell(object):
    def __init__(self, location, type='grass'):
        self.type = type
        self.location = location

