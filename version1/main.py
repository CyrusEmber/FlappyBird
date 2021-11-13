import pyglet
from pyglet.window import key
from load import *


window = pyglet.window.Window(1600, 1000)
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

# pic = pyglet.resource.image('bird.png')
# batch = pyglet.graphics.Batch()
# bird = pyglet.sprite.Sprite(pic, batch=batch)
# bird.update(300, 300)
# score_label = pyglet.text.Label(text="Score: 0", x=10, y=460)
bird = birds()
label = labels()
pillars = pillars()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        bird.velocityY = 300


@window.event
def on_draw():
    window.clear()
    bird.draw()
    label.draw()
    for p in pillars:
        p.draw()


def move(dt, velocity, sprite, gravity=-10, y=0):
    sprite.position += dt * velocity
    y += 1 / 2 * gravity * dt ** 2
    sprite.position = y


def update(dt):
    bird.update(dt)


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
