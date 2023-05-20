import pygame, sys
from src.Settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10) # shrink 5 px from top and bottom
