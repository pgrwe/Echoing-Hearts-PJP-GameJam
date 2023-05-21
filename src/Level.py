import pygame, random
from src.Settings import *
from src.Tile import Tile
from src.Player import Player, Spell, Echoes
from src.Enemy import Enemy
from src.UI import UI

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
        self.enemy_sprites = pygame.sprite.Group()

        # ui setup
        self.ui = UI()

        self.create_map()

        self.enemy_spawn_cooldown = 50


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

    def cursor_display(self):
        pygame.draw.circle(self.display_surface, "blue", self.player.mouse_cursor(), 10)

    def create_echo(self):
        if self.player.playerstates == "hit":
            Echoes(self.player,[self.visible_sprites],self.collision_sprites)
            self.player.playerstates = "recovering"

    def create_spell(self):
        if self.player.spell_cast == True:
            self.spell = Spell(self.player.rect,[self.visible_sprites], self.player.mouse_cursor(), self.enemy_sprites)
            self.player.spell_cast = False

    def enemy_spawner(self):
        if self.enemy_spawn_cooldown <= 0:
            print("A New Enemy Approaches")
            rand_x = random.randint(15, 1250)
            rand_y = random.randint(15, 600)
            self.enemy = Enemy("reaper",(rand_x, rand_y), [self.visible_sprites], self.collision_sprites, self.player)
            self.enemy_sprites.add(self.enemy)
            self.enemy_spawn_cooldown = 50
        self.enemy_spawn_cooldown -= 1

    def render(self):
        '''
        updates and renders to the screen
        '''
        self.create_spell()
        self.create_echo()
        self.enemy_spawner()
        self.background_sprites.camera_draw(self.player)
        self.background_sprites.update()
        self.visible_sprites.camera_draw(self.player)
        self.visible_sprites.update()
        self.ui.ui_render(self.player)

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
