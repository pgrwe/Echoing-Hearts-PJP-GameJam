import pygame
from src.Settings import *
from src.Tile import Tile
from src.Player import Player

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                print(row)
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y),[self.visible_sprites,self.collision_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.visible_sprites],self.collision_sprites)

    def render(self):
        '''
        updates and renders to the screen
        '''
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
