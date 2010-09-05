from __future__ import division
import pyglet
from pyglet.gl import *
from pyglet.window import mouse
from vector import *
from bunny import Bunny
from world import World
from glhelper import *

# TODO: move into window
selection = {'start':None, 'end':None}

def selection_center_radius(selection):
    circle_center = (selection['start'] + selection['end']) / 2
    circle_radius = Length(circle_center - selection['start'])
    return circle_center, circle_radius


class WorldWindow(pyglet.window.Window):
    def __init__(self, world):
        self.world = world
        super(WorldWindow,self).__init__()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            selection['start'] = Vector(x,y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            # select bunnies
            for bunny in world.bunnies:
                bunny.selected = False
            if selection['start'] and selection['end']: 
                circle_center, circle_radius = selection_center_radius(selection)
                for bunny in world.bunnies:
                    distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2), circle_center) 
                    if distance < circle_radius + tile_size/2:
                        bunny.selected = True
            else:
                click_center = Vector(x,y)
                click_radius = tile_size
                for bunny in world.bunnies:
                    distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2) , click_center)
                    if distance < click_radius:
                        bunny.selected = True
            
            selection['start'] = selection['end'] = None

        elif button == mouse.RIGHT:
            # command bunnies
            # lets start with a simple walk to the spot
            for bunny in world.bunnies:
                if bunny.selected:
                    bunny.destination = Vector(int(x / tile_size), int(y / tile_size))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            selection['end'] = Vector(x, y)

    def on_draw(self):
            window.clear()
            world.draw()
            draw_selection()

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

if __name__ == "__main__":
    world = World(Vector(20,20), bunnies=[Bunny(5,7), Bunny(6,9)])
    pyglet.clock.schedule_interval(world.simulate, 0.1)
    window = WorldWindow(world)
    pyglet.app.run()
