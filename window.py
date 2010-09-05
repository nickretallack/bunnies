import pyglet
from selection import Selection
from pyglet.window import mouse
from glhelper import *
class WorldWindow(pyglet.window.Window):
    def __init__(self, world):
        self.world = world
        self.selection = Selection()
        super(WorldWindow,self).__init__()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.selection.start = Vector(x,y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.selection.end = Vector(x,y)
            self.selection.select(self.world)

        elif button == mouse.RIGHT:
            # command bunnies
            for bunny in self.world.bunnies:
                if bunny.selected:
                    bunny.destination = Vector(int(x / tile_size), int(y / tile_size))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.selection.end = Vector(x,y)

    def on_draw(self):
            self.clear()
            self.world.draw()
            self.selection.draw()


