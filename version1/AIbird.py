import bird
from settings import SPACE, JUMP_SPEED
from version1.CGP import create_pop


class AIBird(bird.Bird):
    def __init__(self, individual=None, *args, **kwargs):
        super(AIBird, self).__init__(*args, **kwargs)
        self.individual = individual
        self.individual.find_active_node()
        self.score = 0

    def update(self, dt):
        self.score += 0.1
        super(AIBird, self).update(dt)
        if self.dead:
            self.individual.score = self.score

    def check_flap(self, x, y):
        y_input = self.y - y - SPACE / 2 + 50
        x_input = x - self.x
        if self.individual.eval(x_input, y_input) > 0:
            self.velocityY = JUMP_SPEED
