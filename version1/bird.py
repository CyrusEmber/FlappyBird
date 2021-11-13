import pyglet.sprite


class Bird(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocityX, self.velocityY = 0, 0
        self.accelerationX = 0
        self.accelerationY = -500

    def update(self, dt):
        self.x += self.velocityX * dt
        self.y += self.velocityY * dt
        self.velocityX += self.accelerationX * dt
        self.velocityY += self.accelerationY * dt

    def check_bounds(self):
        # only check y coordinate
        min_y = self.image.height / 2
        max_y = -self.image.height / 2 + 1000
        if self.y < min_y:
            return False
        else:
            if self.y > max_y:
                return False
            else:
                return True




