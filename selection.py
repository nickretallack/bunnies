from glhelper import *

class Selection(object):
    def __init__(self):
        self.start = None
        self.end = None
        self.selected_objects = []

    @property
    def ready(self):
        return self.start is not None and self.end is not None

    @property
    def center_radius(self):
        circle_center = (self.start + self.end) / 2
        circle_radius = Length(circle_center - self.start)
        return circle_center, circle_radius

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

    def select_object(self, it):
        self.selected_objects.append(it)
        it.selected = True

    def deselect_all(self):
        for bunny in self.selected_objects:
            bunny.selected = False
        self.selected_objects = []


    def select(self, world):
        self.deselect_all()

        if self.ready:
            # Dragged a circle
            circle_center, circle_radius = self.center_radius
            for bunny in world.bunnies:
                distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2), circle_center) 
                if distance < circle_radius + tile_size/2:
                    self.select_object(bunny)
        else:
            # Clicked a spot
            click_center = Vector(x,y)
            click_radius = tile_size
            for bunny in world.bunnies:
                distance = Distance(bunny.location * tile_size + Vector(tile_size/2, tile_size/2) , click_center)
                if distance < click_radius:
                    self.select_object(bunny)
        
        self.start = self.end = None
