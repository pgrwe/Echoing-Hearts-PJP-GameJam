import pygame, sys

from pygame.sprite import _Group

class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__(_Group)

