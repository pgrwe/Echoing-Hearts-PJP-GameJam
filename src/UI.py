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

        # need to render hearts and text


        #

    def ui_render(self, player):
        if player.healthpoints > 0:
            for i in range(player.healthpoints):
                self.display_Surface.blit(self.heart,(68,30))
        if player.echo_hearts > 0:
            for i in range(player.echo_hearts):
                # print(player.echo_hearts)
                self.display_Surface.blit(self.echo_heart,(235+(64*i),30))


        self.display_Surface.blit(self.font.render("Hearts",False,(250,250,250)), (54,100))
        self.display_Surface.blit(self.font.render("Echo Hearts",False,(200,200,250)), (260,100))
