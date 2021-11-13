import pyglet.sprite
from pyglet.window import key


class Bird(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocityX, self.velocityY = 0, 0
        self.accelerationX = 0
        self.accelerationY = -800
        self.dead = False
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        self.x += self.velocityX * dt
        self.y += self.velocityY * dt
        self.velocityX += self.accelerationX * dt
        self.velocityY += self.accelerationY * dt
        if self.key_handler[key.SPACE]:
            self.velocityY = 400
        self.check_bounds()

    def check_bounds(self):
        # only check y coordinate
        min_y = self.image.height / 2
        max_y = -self.image.height / 2 + 1000
        if self.y < min_y:
            self.dead = True
        else:
            if self.y > max_y:
                self.y = max_y

    def collide_up(self, sprite):
        # self.y should be lesser than sprite.y
        if abs(self.x - sprite.x) < self.image.width / 2 + sprite.image.width / 2 \
                and -self.y + sprite.y < self.image.height / 2:
            return True
        else:
            return False

    def collide_down(self, sprite):
        # self.y should be greater than sprite.y
        if abs(self.x - sprite.x) < self.image.width / 2 + sprite.image.width / 2 \
                and self.y - sprite.y < self.image.height / 2:
            return True
        else:
            return False



