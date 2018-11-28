import sys
import pygame
import pygame

BLOCK = 10


class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.x = x
        self.y = y

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = BLOCK * self.x
        self.rect.y = BLOCK * self.y


class Game:
    def __init__(self):

        self.width = 21
        self.height = 21
        pygame.init()

        size = self.width * BLOCK, self.height * BLOCK
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(size)

        self.ball = Block((255, 255, 255), BLOCK, BLOCK, 10, 10)
        self.p1 = Block((255, 0, 0), 3 * BLOCK, BLOCK, 9, 0)
        self.p2 = Block((255, 0, 0), 3 * BLOCK, BLOCK, 9, 20)
        self.allsprites = pygame.sprite.RenderPlain(
            (self.p1, self.p2, self.ball))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.black)
            self.allsprites.update()
            self.allsprites.draw(self.screen)
            pygame.display.flip()


class Player:
    def __init__(self):
        self.width = 4


class Ball:
    def __init__(self):
        self.width = 4


if __name__ == '__main__':
    Game().run()
