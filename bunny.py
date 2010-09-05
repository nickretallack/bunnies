from vector import *
from random import random, randint, choice
from glhelper import *

class Bunny(object):
    def __init__(self, world, location, gender):
        self.world = world
        self.location = location
        self.gender = gender
        self.destination = None
        self.mature_age = 20
        self.refractory_period = 10
        self.selected = False
        self.age = self.mature_age
        self.food = 20
        self.chance_to_move = 1
        self.bite_size = 5
        self.food_danger = 5
        self.food_satiated = 30
        self.metabolism = 2
        self.time_since_mated = self.age
        self.pregnant = False
        self.gestation = 0
        self.gestation_period = 10

    x = property(lambda self: self.location.x,
                 lambda self, value: setattr(self.location,'x',value))
    y = property(lambda self: self.location.y,
                 lambda self, value: setattr(self.location,'y',value))

    @property
    def ready_to_mate(self):
        if self.age > self.mature_age:
            if self.gender == 'male' and self.time_since_mated > self.refractory_period:
                return True
            elif self.gender == 'female' and self.pregnant == False:
                return True
        return False

    def mate(self, bunny):
        bunny.pregnant = True
        bunny.gestation = 0
        self.time_since_mated = bunny.time_since_mated = 0

    def give_birth(self):
        self.pregnant = False
        self.gestation = 0
        gender = choice(['male','female'])
        new_bunny = Bunny(self.world, self.location, gender)
        self.world.bunnies.append(new_bunny)

    def step_towards(self, location):
        if location.x < self.x:
            self.x -= 1
        elif location.x > self.x:
            self.x += 1
        if location.y < self.y:
            self.y -= 1
        elif location.y > self.y:
            self.y += 1


    def simulate(self, dt):
        self.age += dt
        self.food -= dt * self.metabolism
        self.time_since_mated += 1 # todo: use timestamps instead
        cell = self.world.get_cell(self.location)

        if self.pregnant:
            self.gestation += dt

        # BEHAVIOR CHOICES
        # TODO: have the bunny make a decision and stick to it,
        # instead of re-calculating every round
        # TODO: model bunnies randomly spreading grass seed

        if self.gestation > self.gestation_period:
            self.give_birth()
            print "birthing",

        elif self.gender == 'male' and self.ready_to_mate:
            # horny buck bunny searches for a mate
            for bunny in self.world.bunnies:
                if bunny.gender == 'female' and bunny.ready_to_mate:
                    if self.location == bunny.location:
                        print "mating",
                        self.mate(bunny)
                    else:
                        print "chasing down mate",
                        self.step_towards(bunny.location)

        elif self.food < 20 and cell.grass > self.bite_size:
            self.food += cell.eat(self.bite_size)
            print "eating",

        # If commanded, follow commands
        elif self.destination:
            if Distance(self.location, self.destination) < 1:
                self.destination = None
                print "finished command",
            else:
                self.step_towards(self.destination)
                print "obeying command",

        elif self.food < self.food_danger:
            if cell.grass:
                self.food += cell.eat(self.bite_size)
                print "eating hungrily",
            else:
                # find a cell with grass and go toward it
                self.step_towards(self.world.nearest_grass(self.location, self.bite_size))
                print "looking for food",

        # If idle, behave randomly
        elif random() < self.chance_to_move:
            print "moving idly",
            new_location = self.location + Vector(randint(-1,1),randint(-1,1))
            new_cell = self.world.get_cell(new_location)
            if new_cell is not None:
                self.location = new_location

        else:
            print "nothing", self.food,

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
