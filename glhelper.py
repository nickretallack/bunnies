from __future__ import division
from contextlib import contextmanager
from pyglet.gl import *
from vector import *
import math

@contextmanager
def matrix():
    glPushMatrix()
    try:
        yield
    finally:
        glPopMatrix()

def draw_square(prim=GL_QUADS):
        pyglet.graphics.draw(4, prim,
        ('v2i', (0, 0, 
                 1, 0,
                 1, 1,
                 0, 1))
        )

def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps):
    verts.append(radius * math.cos(step*1./(steps)*2*math.pi))
    verts.append(radius * math.sin(step*1./(steps)*2*math.pi))
  return verts

tile_size = 30
