from vector import *
from random import random, randint

class Bunny(object):
    def __init__(self, x,y):
        self.location = Vector(x,y)
        self.destination = None
        self.selected = False
        self.age = 0
        self.food = 10
        self.chance_to_move = 0.6

    x = property(lambda self: self.location.x,
                 lambda self, value: setattr(self.location,'x',value))
    y = property(lambda self: self.location.y,
                 lambda self, value: setattr(self.location,'y',value))

    def simulate(self, dt):
        self.age += dt
        self.food -= dt

        # If commanded, follow commands
        if self.destination:
            if Distance(self.location, self.destination) < 2:
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

        # If idle, behave randomly
        elif random() > self.chance_to_move:
            self.x += randint(-1,1)
            self.y += randint(-1,1)

if __name__ == "__main__":
        a = Bunny(1,2)
        a.x
        print a.x, a.y
