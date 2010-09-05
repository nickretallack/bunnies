from __future__ import division
from vector import Vector
from glhelper import *
from bunny import Bunny

width = height = 25

class World(object):
    def __init__(self, size, bunnies=[]):
        self.grid = [[Cell(self, Vector(x,y)) for x in xrange(int(size.x))] 
                                        for y in xrange(int(size.y))]

        self.bunnies = [Bunny(self, Vector(5,7), gender='male'), Bunny(self, Vector(6,9), gender='female')]

        for location in [Vector(5,5), Vector(15,7), Vector(8,13)]:
            self.get_cell(location).grass = 20

    def simulate(self, dt):
        for cell in walk2d(self.grid):
            cell.simulate(dt)

        for bunny in self.bunnies:
            bunny.simulate(dt)
            print '\t| ',
        print

    def draw(self):
        for cell in walk2d(self.grid):
            cell.draw()

        for bunny in self.bunnies:
            bunny.draw()

    def get_cell(self, location):
        if location.x >= 0 and location.y >= 0 and location.y < len(self.grid) and location.x < len(self.grid[0]):
            return self.grid[int(location.y)][int(location.x)]

    def nearest_grass(self, location, min_grass):
        for radius in xrange(len(self.grid)*2):
            for check_location in walk_square(location, radius):
                cell = self.get_cell(check_location)
                if cell is not None and cell.grass > min_grass:
                    return cell.location

class Cell(object):
    def __init__(self, world, location, type='grass'):
        self.type = type
        self.world = world
        self.location = location
        self.grass = 0
        self.grass_max = 20
        self.grass_growth_rate = 0.5

    def simulate(self, dt):
        if self.grass < self.grass_max:
            if self.grass > 0:
                self.grass += dt * self.grass_growth_rate
            else:
                surrounding_grass = sum([cell.grass for cell in self.neighbors])
                if surrounding_grass > self.grass_max / 2:
                    self.grass += dt

            if self.grass > self.grass_max:
                self.grass = self.grass_max

    def eat(self, amount):
        amount_eaten = min(amount, self.grass)
        self.grass -= amount_eaten
        return amount_eaten

    def draw(self):
        with matrix():
            glColor3f(0,self.grass / self.grass_max,0)
            glScalef(tile_size,tile_size,tile_size)
            glTranslatef(self.location.x, self.location.y, 0)
            glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
            draw_square(GL_QUADS)

    @property
    def neighbors(self):
        offsets = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1)]
        found = [self.world.get_cell(self.location + offset) for offset in offsets]
        actual = filter(lambda cell:cell is not None, found)
        return actual

def walk2d(grid):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            yield cell

def walk_square(center, radius):
    for offset in [Vector(x, radius) for x in xrange(-radius, radius)]:
        yield center + offset
    for offset in [Vector(x, -radius) for x in xrange(-radius, radius)]:
        yield center + offset
    for offset in [Vector(radius, y) for y in xrange(-radius, radius)]:
        yield center + offset
    for offset in [Vector(-radius, y) for y in xrange(-radius, radius)]:
        yield center + offset



