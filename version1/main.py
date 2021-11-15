import pyglet
from pyglet.window import key
from pyglet.window.key import MOD_SHIFT
from CGP import Individual, create_pop

from load import *

game_window = pyglet.window.Window(1600, 1000)
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()
pillar_batch = pyglet.graphics.Batch()
ai_batch = pyglet.graphics.Batch()

label = labels(main_batch)
pillars = new_pillar(pillar_batch)
bird = new_birds(main_batch)
ai_bird = new_ai_birds(individual=create_pop(1)[0], batch=ai_batch)
completion = False
score = 0
best_score = 0  # FIXME
time_count = 0
flag = 0
birds_obj = [bird]
ai_birds_obj = [ai_bird]


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
    ai_batch.draw()
    for b in birds_obj:
        game_window.push_handlers(b.get_key_handler())


@game_window.event
def on_key_press(symbol, modifiers):
    # add a new player bird
    if modifiers & MOD_SHIFT:
        if symbol == key.N:
            birds_obj.extend([new_birds(main_batch)])

    # make it faster
    if modifiers & MOD_SHIFT:
        if symbol == key.EQUAL:
            print("speed up")
            pyglet.clock.schedule_interval(update, 1 / 120.0)

    # make it stop
    if modifiers & MOD_SHIFT:
        if symbol == key.BACKSPACE:
            print("stop")
            pyglet.clock.unschedule(update)


def update(dt):
    global completion, score, time_count, flag
    time_count += 1

    # update
    for b in birds_obj:
        b.update(dt)
        # check collide
        if b.collide_down(pillars[0]) or b.collide_up(pillars[1]):
            b.dead = True
    for p in pillars:
        p.update(dt)
    for b in ai_birds_obj:
        b.update(dt)
        if b.collide_down(pillars[0]) or b.collide_up(pillars[1]):
            b.dead = True
        b.check_flap(pillars[0].x, pillars[0].y)

    # check pillars out of bounds
    if pillars[0].check_bounds():
        pillars[0].dead = True
        pillars[1].dead = True

    # remove dead objects
    for to_remove in [obj for obj in pillars if obj.dead]:
        to_remove.delete()
        pillars.remove(to_remove)
    for to_remove in [obj for obj in birds_obj if obj.dead]:
        to_remove.delete()
        birds_obj.remove(to_remove)
    for to_remove in [obj for obj in ai_birds_obj if obj.dead]:
        to_remove.delete()
        ai_birds_obj.remove(to_remove)

    # check AI bird flap


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


if __name__ == '__main__':
    init()
    # init_ai()

    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()
