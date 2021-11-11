import pyglet
from pyglet import shapes

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

circle = shapes.Circle(700, 150, 100, color=(50, 225, 30), batch=batch)

b

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()