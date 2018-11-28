import sys
import pygame
import numpy as np
from neural_network import NeuralNetwork

BLOCK = 10


def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width * BLOCK, height * BLOCK])
        self.image.fill(color)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x = BLOCK * self.x
        self.rect.y = BLOCK * self.y


class Ball(Block):
    def __init__(self):
        Block.__init__(self, (255, 255, 255), 1, 1, 10, 10)
        self.xspeed = -1
        self.yspeed = 1

    def update(self):
        self.x += self.xspeed
        self.y += self.yspeed
        self.move()


class Player(Block):
    def __init__(self, width):
        Block.__init__(self, (255, 0, 0), 2, 1, 7, 0)
        self.screen_width = width

    def set_inputs(self, left, right):
        if left:
            if self.x > 0:
                self.x -= 1
        elif right:
            if self.x < self.screen_width - self.width:
                self.x += 1

    def update(self):
        self.move()


class Game:
    def __init__(self):
        pygame.init()
        self.width = 16
        self.height = 16
        self.clock = pygame.time.Clock()

        self.size = self.width * BLOCK, self.height * BLOCK
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size)

        self.ball = Ball()
        self.p1 = Player(self.width)
        self.player_sprites = [self.p1]
        self.allsprites = pygame.sprite.RenderPlain(
            (self.p1, self.ball))

        self.fitness = 0
        self.highest_fitness = 0

    def reset(self):
        print("Fitness: %i" % self.fitness)
        if(self.fitness > self.highest_fitness):
            self.highest_fitness = self.fitness
        print("Highest Fitness: %i" % self.highest_fitness)
        self.fitness = 0
        self.p1.x = 7
        self.p1.y = 0
        self.ball.x = 10
        self.ball.y = 10

    def run(self):
        for i in range(200):
            print("Offspring %i:" % i)
            nn = NeuralNetwork(12, 2)
            while 1:
                dt = self.clock.tick(15)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                neural_input = bin_array(self.ball.x * 256 +
                                         self.ball.y * 16 + self.p1.x, 12)
                neural_output = nn.feedforward(neural_input).round()
                print(neural_output)
                self.p1.set_inputs(neural_output[0], neural_output[1])

                if(self.detect_collision()):
                    break
                self.allsprites.update()

                self.screen.fill(self.black)
                self.allsprites.draw(self.screen)
                pygame.display.flip()
                self.fitness += 1

    def detect_collision(self):
        if self.ball.x >= self.width - 1:
            self.ball.xspeed *= -1
        if self.ball.y >= self.height - 1:
            self.ball.yspeed *= -1
        if self.ball.x == 0:
            self.ball.xspeed *= -1
        if self.ball.y == 0:
            self.reset()
            return True

        for player in self.player_sprites:
            for i in range(player.width):
                future_x = self.ball.x + self.ball.xspeed
                future_y = self.ball.y + self.ball.yspeed
                if future_x == player.x + i and future_y == player.y:
                    self.ball.yspeed *= -1
        return False


if __name__ == '__main__':
    Game().run()
