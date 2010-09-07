import pyglet
from selection import Selection
from pyglet.window import mouse
from glhelper import *
class WorldWindow(pyglet.window.Window):
    def __init__(self, world, **kwargs):
        self.world = world
        self.selection = Selection()
        super(WorldWindow,self).__init__(**kwargs)

    def on_mouse_press(self, x, y, button, modifiers):
        location = Vector(x,y)
        if button == mouse.LEFT:
            self.selection.start = location

    def on_mouse_release(self, x, y, button, modifiers):
        location = Vector(x,y)
        if button == mouse.LEFT:
            # select bunnies
            self.selection.end = location
            self.selection.select(self.world)

        elif button == mouse.RIGHT:
            # command bunnies
            for bunny in self.selection.selected_objects:
                bunny.destination = tile_coordinate(location)

        elif button == mouse.MIDDLE:
            self.create_grass(location)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        location = Vector(x,y)
        if buttons & mouse.LEFT:
            self.selection.end = location

    def create_grass(self, location):
        tile = tile_coordinate(location)
        cell = self.world.get_cell(tile)
        if cell.grass:
            cell.grass = 0
        else:
            cell.grass = cell.grass_max

    def on_draw(self):
            self.clear()
            self.world.draw()
            self.selection.draw()

def tile_coordinate(location):
    return Vector(int(location.x / tile_size), 
                  int(location.y / tile_size))

