import pygame, math
from src.Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obj_sprites, create_spell):
        super().__init__(groups)
        self.image = pygame.image.load("assets/Vegaslarge.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 8
        self.hitbox  = self.rect.inflate(-6,-10) # removes 3 px from left/right and 5 from top/bottom

        self.obj_sprites = obj_sprites

        # spell cooldown
        self.cooldown = 300
        
        # player resources
        self.casting = False
        self.playerstates = "alive"
        self.create_spell = create_spell
        self.healthpoints = 1

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

        # gets mouse input to determine spellcasts
        self.spell_timer = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.create_spell(self.mouse_cursor())

            
            # self.mouse_cursor()

    def mouse_cursor(self):
        self.mousepos = pygame.mouse.get_pos()
        return self.mousepos

    def move(self, speed):
        # Normalize direction vector so that the speed is the same when moving diagonally
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()
        # moves charcater in direction determined by input keys
        self.hitbox.x += self.dir.x * speed
        self.collision("horiz")
        self.hitbox.y += self.dir.y * speed
        self.collision("vert")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        # collsion stuff related to the ground or other objects (static)
        if direction == "horiz":
            for sprite in self.obj_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.dir.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.dir.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vert":
            for sprite in self.obj_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.dir.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.dir.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def player_state(self):
        print(self.healthpoints)
        print(self.playerstates)

    def update(self):
        self.input()
        self.player_state()
        self.move(self.speed)


class Spell(pygame.sprite.Sprite):
    def __init__(self,player,groups,mousepos):
        super().__init__(groups)
        # load in spell image later self.image = pygame.image.load().convert_alpha()
        self.image = pygame.Surface((10,10))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = player.rect.center)
        self.speed = 15
        self.spell_kill_timer = pygame.time.get_ticks()

        # setup current position vector
        self.rect_vec = pygame.math.Vector2(self.rect.x,self.rect.y)

        # setup up mouse position vector
        self.mouse_vec = pygame.math.Vector2(mousepos)

        # dot product between mouse and pos vectors
        self.dot_product = self.mouse_vec.dot(self.rect_vec)

        # magnitutudes of each vector
        self.mouse_vec_mag = self.mouse_vec.magnitude()
        self.rect_vec_mag = self.mouse_vec.magnitude()

        
        self.angle = (self.dot_product/(self.mouse_vec_mag * self.rect_vec_mag))
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def spellsling(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def update(self):
        # self.spell_cast()
        self.spellsling()
        if pygame.time.get_ticks() >= self.spell_kill_timer + 200:
            self.kill()

class Echoes(pygame.sprite.Sprite):
    def __init__(self,player,groups,mousepos):
        super().__init__(groups)
        # load in spell image later self.image = pygame.image.load().convert_alpha()
        self.image = pygame.Surface((10,10))
        self.image.fill((150,20,87))
        self.rect = self.image.get_rect(center = player.rect.center)
