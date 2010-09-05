from __future__ import division
import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from vector import *
from bunny import Bunny
from world import World
from contextlib import contextmanager

world = World(Vector(20,20))
bunnies = [Bunny(5,7), Bunny(6,9)]
selection = {'start':None, 'end':None}

tile_size = 20
gutter_size = 1

window = pyglet.window.Window()

############# MOVING ###############

def simulate(dt):
    # maybe bunnies should be part of the world?
    for bunny in bunnies:
        bunny.simulate(dt)

    world.simulate(dt)


pyglet.clock.schedule_interval(simulate, 0.1)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        selection['start'] = Vector(x,y)

def selection_center_radius(selection):
    circle_center = (selection['start'] + selection['end']) / 2
    circle_radius = Length(circle_center - selection['start'])
    return circle_center, circle_radius

@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == mouse.LEFT:
        # select bunnies
        for bunny in bunnies:
            bunny.selected = False
        if selection['start'] and selection['end']: 
            circle_center, circle_radius = selection_center_radius(selection)
            for bunny in bunnies:
                distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2), circle_center) 
                if distance < circle_radius + tile_size/2:
                    bunny.selected = True
        else:
            click_center = Vector(x,y)
            click_radius = tile_size
            for bunny in bunnies:
                distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2) , click_center)
                if distance < click_radius:
                    bunny.selected = True
        
        selection['start'] = selection['end'] = None

    elif button == mouse.RIGHT:
        # command bunnies
        # lets start with a simple walk to the spot
        for bunny in bunnies:
            if bunny.selected:
                bunny.destination = Vector(int(x / tile_size), int(y / tile_size))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        selection['end'] = Vector(x, y)

########## DRAWING ###########

@contextmanager
def matrix():
    glPushMatrix()
    try:
        yield
    finally:
        glPopMatrix()

@window.event
def on_draw():
        window.clear()
        draw_board()
        draw_bunnies()
        draw_selection()

def draw_square(prim=GL_QUADS):
        pyglet.graphics.draw(4, prim,
        ('v2i', (0, 0, 
                 1, 0,
                 1, 1,
                 0, 1))
        )

def draw_board():
    for x, row in enumerate(world.grid):
        for y, cell in enumerate(row):
            with matrix():
                glColor3f(0,1.0,0)
                glScalef(tile_size,tile_size,tile_size)
                glTranslatef(x, y, 0)
                glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
                draw_square(GL_QUADS)

def draw_bunnies():
    for bunny in bunnies:
        with matrix():
            if bunny.selected:
                glColor3f(1.0, 0.5, 0.5)
            else:
                glColor3f(1.0, 0, 0)
            glScalef(tile_size,tile_size,tile_size)
            glTranslatef(bunny.x, bunny.y, 0)
            glScalef(1-1/tile_size,1-1/tile_size,1-1/tile_size)
            draw_square(GL_QUADS)

def generate_circle(radius=100, steps=50):
  verts = []
  for step in xrange(steps):
    verts.append(radius * math.cos(step*1./(steps)*2*math.pi))
    verts.append(radius * math.sin(step*1./(steps)*2*math.pi))
  return verts

def draw_selection():
    if selection['start'] and selection['end']:
        center, radius = selection_center_radius(selection)
        vert_count = int(radius / 5.) + 10
        vertices = generate_circle(radius, vert_count)
        with matrix():
            glColor3f(0,0,1.0)
            glTranslatef(center.x, center.y,0)
            pyglet.graphics.draw(vert_count, GL_LINE_LOOP,
                    ('v2f', vertices))

def main():
    pyglet.app.run()

if __name__ == "__main__":
    main()
