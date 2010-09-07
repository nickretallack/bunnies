from vector import *
from random import random, randint, choice
from glhelper import *
import pyglet
from copy import copy

bunny_texture = pyglet.image.load('bunny.png').get_texture()

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
        self.food = 10
        self.chance_to_move = 0.05
        self.bite_size = 5
        self.food_danger = 5
        self.food_satiated = 30
        self.eating_speed = 2
        self.metabolism = 1
        self.time_since_mated = self.age
        self.pregnant = False
        self.gestation = 0
        self.gestation_period = 10
        self.current_action = None
        self.speed = 2
        self.velocity = Vector(0,0)

    @property
    def ready_to_mate(self):
        if self.age > self.mature_age and self.food > self.food_danger:
            if self.gender == 'male' and self.time_since_mated > self.refractory_period:
                return True
            elif self.gender == 'female' and self.pregnant == False:
                return True
        return False

    def mate(self, bunny):
        bunny.pregnant = True
        bunny.gestation = 0
        self.time_since_mated = bunny.time_since_mated = 0

    def step_towards(self, destination, dt):
        self.velocity = Normalize(destination - self.location) * self.speed
        self.location += self.velocity * dt

    def simulate(self, dt):
        self.age += dt
        self.food -= dt * self.metabolism
        self.time_since_mated += 1 # todo: use timestamps instead
        self.cell = self.world.get_cell(self.location)

        if self.pregnant:
            self.gestation += dt

        # BEHAVIOR CHOICES
        # TODO: model bunnies randomly spreading grass seed
        # TODO: model bunny death of old age or starvation

        if not self.current_action:
            for action in actions:
                self.current_action = action.attempt(self)
                if self.current_action:
                    break

        if self.current_action:
            self.current_action.act(dt)
            if self.current_action.finished:
                self.current_action = None

    def draw(self):
        with matrix():
            glBindTexture(bunny_texture.target, bunny_texture.id)
            if self.selected:
                glColor3f(1.0, 0.5, 0.5)
            else:
                glColor3f(1.0, 1.0, 1.0)
            glScalef(*(tile_size,)*3)
            glTranslatef(*self.location)
            glRotatef(Angle(self.velocity),0,0,1)
            glScalef(*(2,)*3)
            glTranslatef(-0.5, -0.5, 0)
            glEnable(GL_TEXTURE_2D)
            draw_textured_square()
            glDisable(GL_TEXTURE_2D)

class Action(object): pass

class Move(Action):
    @classmethod
    def attempt(cls, bunny):
        if random() < bunny.chance_to_move:
            new_location = bunny.location + Vector(randint(-5,5),randint(-5,5))
            new_cell = bunny.world.get_cell(new_location)
            if new_cell is not None:
                print "moving randomly"
                return cls(bunny, new_location)

    def __init__(self, bunny, new_location):
        self.bunny = bunny
        self.destination = new_location

    def act(self, dt):
        self.bunny.step_towards(self.destination, dt)

    @property
    def finished(self):
        return Distance(self.bunny.location, self.destination) < self.bunny.speed

class Eat(Action):
    @classmethod
    def attempt(cls, bunny):
        if bunny.food < 20 and bunny.cell.grass > bunny.bite_size:
            print "begin eating"
            return cls(bunny, bunny.bite_size)
            
    def __init__(self, bunny, quota):
        self.bunny = bunny
        self.quota = quota
        self.finished = False

    def act(self, dt):
        food = self.bunny.cell.eat(self.bunny.eating_speed * dt)
        self.quota -= food
        self.bunny.food += food
        if food < dt or self.quota <= 0:
            self.finished = True

# TODO: make this a compound action
class SearchForFood(Action):
    @classmethod
    def attempt(cls, bunny):
        if bunny.food < bunny.food_danger:
            # find a cell with grass and go toward it
            destination = bunny.world.nearest_grass(bunny.location, bunny.bite_size)
            if bunny.cell.location == destination:
                print 'food here'
                return Eat(bunny, bunny.food_satiated - bunny.food_danger)

            elif destination is None:
                # If no big grasses still exist, go for a small grass
                destination = bunny.world.nearest_grass(bunny.location, 1)
                if bunny.cell.location == destination:
                    print 'desperate food here'
                    return Eat(bunny, bunny.food_satiated - bunny.food_danger)

                elif destination:
                    print 'desperate found'
                    return Move(bunny, destination)
            else:
                print 'found food at %s' % destination
                return Move(bunny, destination)
    
class SearchForMate(Action):
    @classmethod
    def attempt(cls, bunny):
        if bunny.gender == 'male' and bunny.ready_to_mate:
            # horny buck bunny searches for a mate
            for other_bunny in bunny.world.bunnies:
                if other_bunny.gender == 'female' and other_bunny.ready_to_mate:
                    print "searching for a mate"
                    return cls(bunny, other_bunny)

    def __init__(self, bunny, other_bunny):
        self.bunny = bunny
        self.other_bunny = other_bunny
        self.finished = False

    def act(self, dt):
        # It's like move, but we need to re-align to our target.
        if Distance(self.bunny.location, self.other_bunny.location) < self.bunny.speed/2:
            self.bunny.mate(self.other_bunny)
            self.finished = True
            print "mated"
        self.bunny.step_towards(self.other_bunny.location, dt)

class GiveBirth(Action):
    @classmethod
    def attempt(cls, bunny):
        if bunny.gestation > bunny.gestation_period:
            bunny.pregnant = False
            bunny.gestation = 0
            gender = choice(['male','female'])
            new_bunny = Bunny(bunny.world, copy(bunny.location), gender)
            bunny.world.bunnies.append(new_bunny)

actions = [GiveBirth, SearchForFood, SearchForMate, Eat, Move,]

def draw_textured_square(prim=GL_QUADS):
    square = (0, 0,
              1, 0,
              1, 1,
              0, 1)
    
    pyglet.graphics.draw(4, prim,
        ('v2i', square),
        ('t2i', square),
    )