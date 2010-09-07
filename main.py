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
    world = World(Vector(20,20))
    pyglet.clock.schedule_interval(world.simulate, 0.1)
    window = WorldWindow(world, fullscreen=True)

    # when texture area is small, bilinear filter the closest mipmap
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                     GL_LINEAR_MIPMAP_NEAREST );
    # when texture area is large, bilinear filter the original
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
    glEnable (GL_BLEND);
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        


    pyglet.app.run()
