from vector import *
from random import random, randint
from glhelper import *

class Bunny(object):
    def __init__(self, world, location):
        self.world = world
        self.location = location
        self.destination = None
        self.selected = False
        self.age = 0
        self.food = 20
        self.chance_to_move = 0.6
        self.bite_size = 5
        self.food_danger = 10
        self.food_satiated = 20
        self.metabolism = 2

    x = property(lambda self: self.location.x,
                 lambda self, value: setattr(self.location,'x',value))
    y = property(lambda self: self.location.y,
                 lambda self, value: setattr(self.location,'y',value))

    def simulate(self, dt):
        self.age += dt
        self.food -= dt * self.metabolism

        cell = self.world.get_cell(self.location)

        if self.food < 20 and cell.grass > self.bite_size:
            self.food += cell.eat(self.bite_size)

        # If commanded, follow commands
        elif self.destination:
            if Distance(self.location, self.destination) < 1:
                self.destination = None
            else:
                if self.destination.x < self.x:
                    self.x -= 1
                elif self.destination.x > self.x:
                    self.x += 1
                if self.destination.y < self.y:
                    self.y -= 1
                elif self.destination.y > self.y:
                    self.y += 1

        elif self.food < 10:
            if cell.grass:
                self.food += cell.eat(self.bite_size)
            else:
                # find a cell with grass and go toward it
                self.destination = self.world.nearest_grass(self.location, self.bite_size)

        # If idle, behave randomly
        elif random() > self.chance_to_move:
            new_location = self.location + Vector(randint(-1,1),randint(-1,1))
            new_cell = self.world.get_cell(new_location)
            if new_cell is not None:
                self.location = new_location

    def draw(self):
        with matrix():
            if self.selected:
                glColor3f(1.0, 0.5, 0.5)
            else:
                glColor3f(1.0, 0, 0)
            glScalef(tile_size,tile_size,tile_size)
            glTranslatef(self.x, self.y, 0)
            glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
            draw_square(GL_QUADS)

if __name__ == "__main__":
        a = Bunny(1,2)
        a.x
        print a.x, a.y
