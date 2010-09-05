# Fond memories of code that could have been.

from vector import *
class Bunny(object):
    def __init__(self, x,y):
        self.location = Vector(x,y)
        self.destination = None
        self.selected = False
        
        # Tried to implement x and y properties this way, but unfortunately
        # the lambdas both took the same 'attribute'.  I'm not sure why this happens.
        for attribute in 'x y'.split():
            setattr(self.__class__, attribute, property(
                    lambda self: getattr(self.location, attribute),
                    lambda self, value: setattr(self.location, attribute, value)))

    # My first attempt at the properties ended up causing bugs in other attributes,
    # so I decided to use properties instead.
    def __getattr__(self, attr):
        if attr in 'x y'.split():
            getattr(self.location, attr)

    def __setattr__(self, attr, value):
        if attr in 'x y'.split():
            setattr(self.location, attr, value)
        else:
            self.__dict__[attr] = value

if __name__ == "__main__":
        a = Bunny(1,2)
        a.x
        print a.x, a.y

