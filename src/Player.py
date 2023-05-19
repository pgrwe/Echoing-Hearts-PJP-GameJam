import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.image = pygame.image.load("image")
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()

    def move(self):
        input = pygame.key.get_pressed()

        if input[pygame.K_UP]:
            self.dir.y = -1
        elif input[pygame.K_DOWN]:
            self.dir.y = 1
        else:
            self.dir.y = 0

        if input[pygame.K_RIGHT]:
            self.dir.x = -1
        elif input[pygame.K_LEFT]:
            self.dir.x = 1
        else:
            self.dir.x = 0

    def update(self):
        self.move()
