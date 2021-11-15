import time

import pyglet
import random
import bird
import pillar
import AIbird
from settings import SPACE
from version1.CGP import create_pop

pyglet.resource.path = ['../assets']
pyglet.resource.reindex()
_WIDTH = 1600
_HEIGHT = 1000


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def center_low_pillar(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height


def center_high_pillar(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = 0


def new_birds(batch=None):
    bird_image = pyglet.resource.image('bird.png')
    bird_image.width = 100
    bird_image.height = 100
    center_image(bird_image)
    new_bird = bird.Bird(bird_image, x=200, y=500, batch=batch)
    # print(new_bird.height) = 100
    return new_bird


def labels(batch=None):
    score_label = pyglet.text.Label(text="Score: 0", x=10, y=500, batch=batch)
    return score_label


def new_pillar(batch=None):
    # without acceleration
    pillar_low_image = pyglet.resource.image('downPillar.png')
    pillar_high_image = pyglet.resource.image('upPillar.png')
    pillar_low_image.width = 150
    pillar_high_image.width = 150
    pillar_low_image.height = 1000
    pillar_high_image.height = 1000
    center_low_pillar(pillar_low_image)
    center_high_pillar(pillar_high_image)
    new_pillars = [0]*2
    # while game_fail:
    #     time.sleep(2)
    new_pillar_lower = random.randint(100, _HEIGHT - 300)
    new_pillars[0] = pillar.Pillar(pillar_low_image, x=_WIDTH + pillar_low_image.width / 2, y=new_pillar_lower, batch=batch)
    new_pillars[1] = pillar.Pillar(pillar_high_image, x=_WIDTH + pillar_low_image.width / 2, y=new_pillar_lower + SPACE, batch=batch)
    return new_pillars


def new_ai_birds(individual, batch=None):
    bird_image = pyglet.resource.image('bird.png')
    bird_image.width = 100
    bird_image.height = 100
    center_image(bird_image)
    new_bird = AIbird.AIBird(img=bird_image, individual=individual, x=200, y=500, batch=batch)

    return new_bird


def game_fail(player_bird):
    return player_bird.check_bounds()
