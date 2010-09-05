from vector import *
class Bunny(object):
    def __init__(self, x,y):
        self.location = Vector(x,y)
        self.destination = None
        self.selected = False

    x = property(lambda self: self.location.x,
                 lambda self, value: setattr(self.location,'x',value))
    y = property(lambda self: self.location.y,
                 lambda self, value: setattr(self.location,'y',value))


if __name__ == "__main__":
        a = Bunny(1,2)
        a.x
        print a.x, a.y
