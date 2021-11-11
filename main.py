import pyglet

from Bird import Bird

window = pyglet.window.Window(1600, 1000)
bird = Bird(300, 300)


@window.event
def on_draw():
    window.clear()
    bird.batch.draw()


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

if __name__ == '__main__':
    pyglet.app.run()
