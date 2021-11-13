import pyglet
from pyglet.window import key
from load import *

game_window = pyglet.window.Window(1600, 1000)
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()
label = labels(main_batch)
pillars = new_pillar(main_batch)
bird = birds(main_batch)
completion = False
score = 0
time_count = 0
flag = 0
birds = [bird]


def init():
    global score
    score = 0
    label.text = "Score: " + str(score)


@game_window.event
def on_draw():
    global completion
    game_window.clear()
    main_batch.draw()
    if not completion:
        game_window.push_handlers(bird.key_handler)


def update(dt):
    global completion, score, time_count, flag
    player_dead = False
    time_count += 1

    # update
    for b in birds:
        b.update(dt)
        # check collide
        if b.collide_down(pillars[0]) or b.collide_up(pillars[1]):
            b.dead = True
    for p in pillars:
        p.update(dt)

    # check pillars out of bounds
    if pillars[0].check_bounds():
        pillars[0].dead = True
        pillars[1].dead = True
    for to_remove in [obj for obj in pillars if obj.dead]:
        to_remove.delete()
        pillars.remove(to_remove)
    for to_remove in [obj for obj in birds if obj.dead]:
        to_remove.delete()
        birds.remove(to_remove)

    # add new pillars and reset flag for score
    if time_count % 240 == 0:
        flag = 0
        add_pillars = new_pillar(main_batch)
        pillars.extend(add_pillars)

    # score
    if pillars[0].check_score() and flag == 0 and len(birds) > 0:
        # print(time_count)
        flag += 1
        score += 1
        label.text = "Score: " + str(int(score))


# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
