import pygame
from src.Settings import *
from src.Tile import Tile
from src.Player import Player, Spell
from src.Enemy import Enemy

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                print(row)
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    # spawns tiles
                    Tile((x,y),[self.visible_sprites,self.collision_sprites])
                if col == 'p':
                    # spawns player
                    self.player = Player((x,y),[self.visible_sprites],self.collision_sprites,self.create_spell)
                if col == 'r':
                    # spawns reaper
                    self.enemy = Enemy("reaper",(x,y), [self.visiblie_sprites])

    def create_spell(self):
        Spell(self.player,[self.visible_sprites])

    def cursor_display(self):
        pygame.draw.circle(self.display_surface, "blue", self.player.mouse_cursor(), 10)

    def render(self):
        '''
        updates and renders to the screen
        '''
        self.visible_sprites.camera_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup to put character in middle of the screen at all times
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(100,200)

    def camera_draw(self, player):
        # calculating offset for camera centering
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
