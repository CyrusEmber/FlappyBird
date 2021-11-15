import pyglet
from pyglet import shapes, window
from pyglet import clock
from pyglet.window import key
from pyglet import image


class Bird:
    """
    bird should be stationary in x coordinates
    """
    pyglet.resource.path = ['assets']
    pyglet.resource.reindex()

    def __init__(self, x, y):
        pic = pyglet.resource.image('bird.png')
        self.dt = clock.tick()
        self.x = x
        self.y = y

        self.batch = pyglet.graphics.Batch()
        # circle = shapes.Circle(x, y, 100, color=(50, 225, 30), batch=self.batch)
        bird = pyglet.sprite.Sprite(pic, batch=self.batch)

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.SPACE:
                self.velocity = 20

        clock.schedule(self.move, bird)

    def move(self, sprite, gravity=-10):
        self.y += 1 / 2 * gravity * self.dt ** 2
        sprite.position = self.y
