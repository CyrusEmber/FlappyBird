import pyglet
from pyglet.window import key
from pyglet.window.key import MOD_SHIFT
from CGP import Individual, create_pop, evolve

from load import *

game_window = pyglet.window.Window(1600, 1000)
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()
pillar_batch = pyglet.graphics.Batch()
ai_batch = pyglet.graphics.Batch()

label_score = labels(batch=main_batch)
label_alive = labels(y=520, batch=main_batch)
label_best = labels(y=540, batch=main_batch)
label_generation = labels(y=560, batch=main_batch)
pillars = new_pillar(pillar_batch)

completion = False
score = 0
best_score = 0  # FIXME
time_count = 0
flag = 0
alive = 0
generation = 1
ai_num = ""
pop = None

birds_obj = []
ai_birds_obj = []


def create_ai_bird(pops):
    global alive, ai_num
    for ind in pops:
        ai_birds_obj.append(new_ai_birds(individual=ind, batch=ai_batch))
        alive += 1
    ai_num = str(alive)


def clear_game():
    global pillars, generation, score, time_count
    for obj in pillars:
        obj.delete()
        pillars.remove(obj)
    for obj in birds_obj:
        obj.delete()
        birds_obj.remove(obj)
    generation += 1
    score = 0
    time_count = 0
    pillars = new_pillar(pillar_batch)


def init():
    global birds_obj, score

    score = 0
    label_score.text = "Score: " + str(score)

    birds_obj.append(new_birds(main_batch))


def init_pop():
    global ai_birds_obj, alive, ai_num, pop
    pop = create_pop(10)
    create_ai_bird(pop)
    label_alive.text = "Alive: " + str(alive) + "/" + ai_num
    label_generation.text = "Generation: " + str(generation)
    label_best.text = "Best score: " + str(best_score)


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
    global completion, score, time_count, flag, alive, pop, best_score
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
        if b.collide_down(pillars[0]) or b.collide_up(pillars[1]):
            b.dead = True
        b.update(dt)
        # flap or not
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
        alive -= 1
        to_remove.delete()
        ai_birds_obj.remove(to_remove)

    # add new pillars and reset flag for score
    if time_count % 240 == 0:
        time_count = 0
        flag = 0
        add_pillars = new_pillar(pillar_batch)
        pillars.extend(add_pillars)

# label
    # score
    if flag == 0 and (len(birds_obj) > 0 or len(ai_birds_obj) > 0) and pillars[0].check_score():
        # print(time_count)
        flag += 1
        score += 1
        label_score.text = "Score: " + str(int(score))
    # check alive AI
    label_alive.text = "Alive: " + str(alive) + "/" + ai_num
    # check best score
    if score > best_score:
        best_score = score
        label_best.text = "Best score: " + str(best_score)
    # check generation
    label_generation.text = "Generation: " + str(generation)

    # evolve AI
    if alive == 0:
        pop = evolve(pop, 0.03, 4, 6)
        clear_game()
        create_ai_bird(pop)


if __name__ == '__main__':
    init()
    init_pop()
    # init_ai()

    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()
