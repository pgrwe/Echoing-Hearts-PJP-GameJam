import pygame 
from src.Settings import *
from src.Player import Player

class UI:
    def __init__(self):
        # general
        self.display_Surface =  pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # hearts
        self.heart = pygame.image.load(UI_HEART_IMAGE)
        self.echo_heart = pygame.image.load(UI_ECHO_HEART_IMAGE)


        #
    
    def ui_render(self, player):
        pass
