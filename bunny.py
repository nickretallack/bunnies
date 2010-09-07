from vector import *
from random import random, randint, choice
from glhelper import *
import pyglet

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
        self.metabolism = 1
        self.time_since_mated = self.age
        self.pregnant = False
        self.gestation = 0
        self.gestation_period = 10
        self.current_action = None
        self.speed = 0.1
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

    def give_birth(self):
        if self.gestation > self.gestation_period:
            self.pregnant = False
            self.gestation = 0
            gender = choice(['male','female'])
            new_bunny = Bunny(self.world, self.location, gender)
            self.world.bunnies.append(new_bunny)
            print "birthing",
            return True

    def step_towards(self, location):
        self.velocity = Normalize(location - self.location) * self.speed
        self.location += self.velocity

    def male_search_for_mate(self):
        if self.gender == 'male' and self.ready_to_mate:
            # horny buck bunny searches for a mate
            for bunny in self.world.bunnies:
                if bunny.gender == 'female' and bunny.ready_to_mate:
                    if self.location == bunny.location:
                        self.mate(bunny)
                        print "mating",
                        return True
                    else:
                        self.step_towards(bunny.location)
                        print "chasing mate",
                        return True

    def do_nothing(self):
        print "doing nothing",
        return True

    def simulate(self, dt):
        self.age += dt
        self.food -= dt * self.metabolism
        self.time_since_mated += 1 # todo: use timestamps instead
        self.cell = self.world.get_cell(self.location)

        if self.pregnant:
            self.gestation += dt

        # BEHAVIOR CHOICES
        # TODO: have the bunny make a decision and stick to it,
        # instead of re-calculating every round
        # TODO: model bunnies randomly spreading grass seed
        # TODO: model bunny death of old age or starvation
        # TODO: add another action for desperately eating the last of 

        if not self.current_action:
            for action in actions:
                self.current_action = action.attempt(self)
                if self.current_action:
                    break

        if self.current_action:
            self.current_action.act()
            if self.current_action.finished:
                self.current_action = None

        """
        for action in [self.give_birth, self.follow_orders, self.male_search_for_mate, self.eat_food_here,
                self.search_for_food, self.move_randomly, self.do_nothing]:
            success = action()
            if success:
                break
        """

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

    def act(self):
        self.bunny.step_towards(self.destination)

    @property
    def finished(self):
        return Distance(self.bunny.location, self.destination) < self.bunny.speed

class EatFoodHere(Action):
    @classmethod
    def attempt(cls, bunny):
        if bunny.food < 20 and bunny.cell.grass > bunny.bite_size:
            print "begin eating"
            return cls(bunny, bunny.bite_size)
            
    def __init__(self, bunny, quota):
        self.bunny = bunny
        self.quota = quota
        self.finished = False

    def act(self):
        food = self.bunny.cell.eat(1)
        self.quota -= food
        self.bunny.food += food
        if food < 1 or self.quota <= 0:
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
                return EatFoodHere(bunny, bunny.food_satiated - bunny.food_danger)

            elif destination is None:
                # If no big grasses still exist, go for a small grass
                destination = self.world.nearest_grass(self.location, 1)
                if self.cell.location == destination:
                    print 'desperate food here'
                    return EatFoodHere(bunny, bunny.food_satiated - bunny.food_danger)

                elif destination:
                    print 'desperate found'
                    return Move(bunny, destination)
            else:
                #import pdb; pdb.set_trace()
                print 'found food at %s' % destination
                return Move(bunny, destination)
    

actions = [SearchForFood, EatFoodHere, Move,]


def draw_textured_square(prim=GL_QUADS):
    square = (0, 0,
              1, 0,
              1, 1,
              0, 1)
    
    pyglet.graphics.draw(4, prim,
        ('v2i', square),
        ('t2i', square),
    )




if __name__ == "__main__":
        a = Bunny(1,2)
        a.x
        print a.x, a.y
