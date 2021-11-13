import pyglet
from pyglet.window import key
from pyglet.window.key import MOD_SHIFT

from load import *

game_window = pyglet.window.Window(1600, 1000)
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()
pillar_batch = pyglet.graphics.Batch()

label = labels(main_batch)
pillars = new_pillar(pillar_batch)
bird = new_birds(main_batch)
completion = False
score = 0
time_count = 0
flag = 0
birds_obj = [bird]


def init():
    global score
    score = 0
    label.text = "Score: " + str(score)


@game_window.event
def on_draw():
    global completion
    game_window.clear()
    main_batch.draw()
    pillar_batch.draw()
    for b in birds_obj:
        game_window.push_handlers(b.key_handler)


@game_window.event
def on_key_press(symbol, modifiers):
    if modifiers & MOD_SHIFT:
        if symbol == key.N:
            birds_obj.extend([new_birds(main_batch)])


def update(dt):
    global completion, score, time_count, flag, pillars_obj
    time_count += 1
    print(len(pillars))

    # update
    for b in birds_obj:
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
    for to_remove in [obj for obj in birds_obj if obj.dead]:
        to_remove.delete()
        birds_obj.remove(to_remove)

    # add new pillars and reset flag for score
    if time_count % 240 == 0:
        time_count = 0
        flag = 0
        add_pillars = new_pillar(pillar_batch)
        pillars.extend(add_pillars)

    # score
    if flag == 0 and len(birds_obj) > 0 and pillars[0].check_score():
        # print(time_count)
        flag += 1
        score += 1
        label.text = "Score: " + str(int(score))


def update_pillar():
    global pillars_obj
    # add new pillars and reset flag for score
    if time_count % 240 == 0:
        add_pillars = new_pillar(pillar_batch)
        pillars.extend(add_pillars)


if __name__ == '__main__':
    init()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
