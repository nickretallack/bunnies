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
        self.food = 0
        self.chance_to_move = 1
        self.bite_size = 5
        self.food_danger = 5
        self.food_satiated = 30
        self.metabolism = 5
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
        if location.x < self.x:
            self.x -= 1
        elif location.x > self.x:
            self.x += 1
        if location.y < self.y:
            self.y -= 1
        elif location.y > self.y:
            self.y += 1

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

    def eat_food_here(self):
        if self.food < 20 and self.cell.grass > self.bite_size:
            self.food += self.cell.eat(self.bite_size)
            print "eating",
            return True

    def follow_orders(self):
        if self.destination:
            self.step_towards(self.destination)
            if Distance(self.location, self.destination) < 1:
                self.destination = None
            print "obeying command",
            return True

    def search_for_food(self):
        if self.food < self.food_danger:
            # find a cell with grass and go toward it
            destination = self.world.nearest_grass(self.location, self.bite_size)
            if self.cell.location == destination:
                self.food += self.cell.eat(self.bite_size)
                print "eating hungrily",
                return True
            elif destination is None:
                # If no big grasses still exist, go for a small grass
                destination = self.world.nearest_grass(self.location, 1)
                if self.cell.location == destination:
                    self.food += self.cell.eat(self.bite_size)
                    print "eating desperately",
                    return True
                elif destination:
                    self.step_towards(destination)
                    print "looking desperately for food"
                    return True
            else:
                self.step_towards(destination)
                print "looking for food",
                return True

    def move_randomly(self):
        if random() < self.chance_to_move:
            new_location = self.location + Vector(randint(-1,1),randint(-1,1))
            new_cell = self.world.get_cell(new_location)
            if new_cell is not None:
                self.location = new_location
                print "moving randomly",
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

        for action in [self.give_birth, self.follow_orders, self.male_search_for_mate, self.eat_food_here,
                self.search_for_food, self.move_randomly, self.do_nothing]:
            success = action()
            if success:
                break

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
