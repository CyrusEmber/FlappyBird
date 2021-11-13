import time

import pyglet
import random

from pyglet import shapes

import bird
import pillar

pyglet.resource.path = ['../assets']
pyglet.resource.reindex()
_WIDTH = 1600
_HEIGHT = 1000


def birds():
    new_bird = bird.Bird(pyglet.resource.image('bird.png'), x=300, y=300)
    new_bird.scale = 0.5
    # print(new_bird.height) = 95
    return new_bird


def labels():
    score_label = pyglet.text.Label(text="Score: 0", x=10, y=500)
    return score_label


def pillars():
    # without acceleration
    new_pillars = []
    # while game_fail:
    #     time.sleep(2)
    new_pillar_lower = random.randint(100, _HEIGHT - 100)
    square_low = shapes.Rectangle(x=_WIDTH, y=200, width=200, height=new_pillar_lower, color=(0, 0, 0))
    square_high = shapes.Rectangle(x=_WIDTH, y=800, width=200, height=_HEIGHT - new_pillar_lower, color=(0, 0, 0))
    new_pillars[0] = pillar.Pillar(square_low, x=_WIDTH, y=200)
    new_pillars[1] = pillar.Pillar(square_low, x=_WIDTH, y=800)

    return new_pillars


def game_fail(player_bird):
    return player_bird.check_bounds()
