import pygame
# from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obj_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("assets/Vegaslarge.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 5
        self.obj_sprites = obj_sprites

        # player resources
        self.healthpoints = 1
        self.echoes = 0

    def input(self):
        # gets input keys to determine direction
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dir.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dir.y = 1
        else:
            self.dir.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dir.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dir.x = -1
        else:
            self.dir.x = 0

    def move(self, speed):
        # Normalize direction vector so that the speed is the same when moving diagonally
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()
        # moves charcater in direction determined by input keys
        self.rect.x += self.dir.x * speed
        self.collision("horiz")
        self.rect.y += self.dir.y * speed
        self.collision("vert")


    def collision(self, direction):
        # collsion stuff related to the ground or other objects (static)
        if direction == "horiz":
            for sprite in self.obj_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.dir.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    if self.dir.x < 0: # moving left
                        self.rect.left = sprite.rect.right

        if direction == "vert":
            for sprite in self.obj_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.dir.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.dir.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
    

class Arrow:
    def __init__(self, x, y, mousepos):
        pass
