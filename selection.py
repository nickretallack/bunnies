from glhelper import *

class Selection(object):
    def __init__(self):
        self.start = None
        self.end = None

    @property
    def ready(self):
        return self.start is not None and self.end is not None

    @property
    def center_radius(self):
        circle_center = (self.start + self.end) / 2
        circle_radius = Length(circle_center - self.start)
        return circle_center, circle_radius

    def clear(self):
        self.start = self.end = None

    def draw(self):
        if self.ready:
            center, radius = self.center_radius
            vert_count = int(radius / 5.) + 10
            vertices = generate_circle(radius, vert_count)
            with matrix():
                glColor3f(0,0,1.0)
                glTranslatef(center.x, center.y,0)
                pyglet.graphics.draw(vert_count, GL_LINE_LOOP,
                        ('v2f', vertices))

    def select(self, world):
        # select bunnies
        for bunny in world.bunnies:
            bunny.selected = False
        if self.ready:
            circle_center, circle_radius = self.center_radius
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
        
        self.clear()
