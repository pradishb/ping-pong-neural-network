import sys
import pygame
from abc import abstractmethod

BLOCK = 10


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

    @abstractmethod
    def move(self):
        pass

    def update(self):
        self.move()
        self.rect.x = BLOCK * self.x
        self.rect.y = BLOCK * self.y

# class Player(Block):
#     def __init__(self):
#         super()


class Ball(Block):
    def __init__(self):
        Block.__init__(self, (255, 255, 255), 1, 1, 10, 10)
        self.xspeed = -1
        self.yspeed = -1

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed


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
        self.p1 = Block((255, 0, 0), 2, 1, 7, 0)
        self.p2 = Block((255, 0, 0), 2, 1, 14, self.height-1)
        self.player_sprites = [self.p1, self.p2]
        self.allsprites = pygame.sprite.RenderPlain(
            (self.p1, self.p2, self.ball))

    def run(self):
        while 1:
            dt = self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            print(self.p1.x)

            self.screen.fill(self.black)
            self.detect_collision()
            self.allsprites.update()
            self.allsprites.draw(self.screen)
            pygame.display.flip()

    def detect_collision(self):
        if self.ball.x >= self.width - 1:
            self.ball.xspeed *= -1
        if self.ball.y >= self.height - 1:
            self.ball.yspeed *= -1
        if self.ball.x == 0:
            self.ball.xspeed *= -1
        if self.ball.y == 0:
            self.ball.yspeed *= -1

        for player in self.player_sprites:
            for i in range(player.width):
                future_x = self.ball.x + self.ball.xspeed
                future_y = self.ball.y + self.ball.yspeed
                if future_x == player.x + i and future_y == player.y:
                    self.ball.yspeed *= -1


if __name__ == '__main__':
    Game().run()
