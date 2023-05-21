import pygame
from src.Settings import *
from src.Tile import Tile
from src.Player import Player, Spell, Echoes
from src.Enemy import Enemy

class Level:
    def __init__(self):
        # loading tile assets
        self.front_wall = pygame.image.load("assets/terrain/wall_mid.png")
        self.right_wall = pygame.image.load("assets/terrain/wall_outer_front_right.png")
        self.left_wall = pygame.image.load("assets/terrain/wall_outer_front_left.png")
        self.floor = pygame.image.load("assets/terrain/floor.png")
        # get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.background_sprites = CameraGroup()
        self.spell_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.create_map()


    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                # Spawns tiles
                if col == 'x':
                    Tile(self.front_wall,(x,y),[self.visible_sprites,self.collision_sprites])
                if col == 'l':
                    Tile(self.left_wall,(x,y),[self.visible_sprites,self.collision_sprites])
                if col == 'r':
                    Tile(self.right_wall,(x,y),[self.visible_sprites,self.collision_sprites])
                if col == ' ':
                    Tile(self.floor,(x,y),self.background_sprites)

                # Creature spawns
                if col == 'p':
                    Tile(self.floor,(x,y),self.background_sprites)
                    # spawns player
                    # self.player = Player((x,y),[self.visible_sprites],self.collision_sprites,self.create_spell)
                    self.player = Player((x,y),[self.visible_sprites],self.collision_sprites)
                if col == 'e':
                    # spawns reaper
                    Tile(self.floor,(x,y),self.background_sprites)
                    self.enemy = Enemy("reaper",(x,y), [self.visible_sprites], self.collision_sprites, self.player)

    def cursor_display(self):
        pygame.draw.circle(self.display_surface, "blue", self.player.mouse_cursor(), 10)

    def create_echo(self):
        if self.player.playerstates == "hit":
            Echoes(self.player,[self.visible_sprites],self.collision_sprites)
            self.player.playerstates = "recovering"

    def create_spell(self):
        if self.player.spell_cast == True:
            Spell(self.player.rect,[self.visible_sprites], self.player.mouse_cursor())
            self.player.spell_cast = False

    def render(self):
        '''
        updates and renders to the screen
        '''
        self.create_spell()
        self.create_echo()
        self.background_sprites.camera_draw(self.player)
        self.background_sprites.update()
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

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(100,200)

    def camera_draw(self, player):
        # calculating offset for camera centering
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    # def enemy_update(self, player)
    #     enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
    #     for enemy in enemy_sprites:
