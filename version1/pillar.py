import pyglet


class Pillar(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocityX, self.velocityY = -300, 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.dead = False

    def update(self, dt):
        self.x += self.velocityX * dt
        self.y += self.velocityY * dt
        self.velocityX += self.accelerationX * dt
        self.velocityY += self.accelerationY * dt

    def check_bounds(self):
        # only check y coordinate
        min_x = - self.image.width * self.scale / 2
        if self.x < min_x:
            return True
        else:
            return False

    def check_score(self):
        # only check y coordinate

        min_x = - self.image.width * self.scale / 2 + 100
        if int(self.x) < int(min_x):
            return True
        else:
            return False

