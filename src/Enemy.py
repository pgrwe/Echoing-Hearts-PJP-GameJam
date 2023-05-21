import pygame, math
from src.Player import Player, Echoes
# attack_radius = collision
# notice_radius = infinite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, obj_sprites, player):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.image = pygame.image.load("assets/Vegaslarge.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 2
        self.hitbox  = self.rect.inflate(-6,-10) # removes 3 px from left/right and 5 from top/bottom

        self.obj_sprites = obj_sprites
        self.player = player
        self.target_pos = self.player.hitbox
        self.attack_radius = 120
        self.notice_radius = 400

    def chase(self):
        if self.target_pos.y > self.hitbox.y:
            self.dir.y = 1
        elif self.target_pos.y < self.hitbox.y:
            self.dir.y = -1
        else:
            self.dir.y = 0

        if self.target_pos.x > self.hitbox.x:
            self.dir.x = 1
        elif self.target_pos.x < self.hitbox.x:
            self.dir.x = -1
        else:
            self.dir.x = 0

    def move(self, speed):
        # Normalize direction vector so that the speed is the same when moving diagonally
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()
        # moves character in direction determined by random
        self.hitbox.x += self.dir.x * speed
        self.collision("horiz")
        self.fight("horiz")
        self.hitbox.y += self.dir.y * speed
        self.collision("vert")
        self.fight("vert")
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

    def fight(self, direction):
        # collision with Player
        if direction == "horiz":
            if self.hitbox.colliderect(self.target_pos):
                print("ouch")
                self.player.healthpoints -= 1
                self.player.playerstates = "hit"
                self.player.player_time = pygame.time.get_ticks()
                if self.dir.x > 0: # moving right
                    self.hitbox.right = self.hitbox.left
                if self.dir.x < 0: # moving left
                    self.hitbox.left = self.hitbox.right

        if direction == "vert":
            if self.hitbox.colliderect(self.target_pos):
                print("ouch") 
                self.player.healthpoints -= 1
                self.player.playerstates = "hit"
                self.player.player_time = pygame.time.get_ticks()
                if self.dir.y > 0: # moving down
                    self.hitbox.bottom = self.hitbox.top
                if self.dir.y < 0: # moving up
                    self.hitbox.top = self.hitbox.bottom


    def update(self):
        if self.player.playerstates == "alive":
            self.chase()
            self.move(self.speed)
