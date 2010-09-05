from __future__ import division
import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from vector import *
from bunny import Bunny
from world import World
from window import WorldWindow
from glhelper import *


if __name__ == "__main__":
    world = World(Vector(20,20), bunnies=[Bunny(5,7), Bunny(6,9)])
    pyglet.clock.schedule_interval(world.simulate, 0.1)
    window = WorldWindow(world)
    pyglet.app.run()
