import pygame, math
from src.Player import Player, Echoes
# attack_radius = collision
# notice_radius = infinite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, obj_sprites, player):
        super().__init__(groups)

        self.enemy_run_right = []
        self.enemy_run_right.append(pygame.image.load("assets/echoenemy/enemy1.png"))
        self.enemy_run_right.append(pygame.image.load("assets/echoenemy/enemy2.png"))
        self.enemy_run_right.append(pygame.image.load("assets/echoenemy/enemy3.png"))
        self.enemy_run_right.append(pygame.image.load("assets/echoenemy/enemy4.png"))

        self.enemy_run_left = []
        self.enemy_run_left.append(pygame.transform.flip(self.enemy_run_right[0], True, False))
        self.enemy_run_left.append(pygame.transform.flip(self.enemy_run_right[1], True, False))
        self.enemy_run_left.append(pygame.transform.flip(self.enemy_run_right[2], True, False))
        self.enemy_run_left.append(pygame.transform.flip(self.enemy_run_right[3], True, False))

        self.current_frame = 0
        self.animation_state = "run_right"
        self.facing = "right"
        self.image = self.enemy_run_left[self.current_frame]


        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 2
        self.hitbox  = self.rect.inflate(-4,-8) # removes 3 px from left/right and 5 from top/bottom

        self.obj_sprites = obj_sprites
        self.player = player
        self.target_pos = self.player.hitbox
        self.healthpoints = 10
        self.state = "chase"

    def chase(self):
        if self.target_pos.y > self.hitbox.y:
            self.dir.y = 1
            if self.facing == "right" and self.dir.x == 0:
                self.animation_state = "run_right"
            elif self.facing == "left" and self.dir.x == 0:
                self.animation_state = "run_left"
        elif self.target_pos.y < self.hitbox.y:
            if self.facing == "right" and self.dir.x == 0:
                self.animation_state = "run_right"
            elif self.facing == "left" and self.dir.x == 0:
                self.animation_state = "run_left"
        else:
            self.dir.y = 0

        if self.target_pos.x > self.hitbox.x:
            self.dir.x = 1
            self.animation_state = "run_right"
            self.facing = "right"
        elif self.target_pos.x < self.hitbox.x:
            self.dir.x = -1
            self.animation_state = "run_left"
            self.facing = "left"
        else:
            self.dir.x = 0

    def move(self, speed):
        # Normalize direction vector so that the speed is the same when moving diagonally
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()
        
        # moves enemy towards player
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
                self.player.healthpoints -= 1
                if self.player.healthpoints <= 0:
                    self.player.playerstates = "dying"
                else:
                    self.player.playerstates = "hit"
                self.player.player_time = pygame.time.get_ticks()
                if self.dir.x > 0: # moving right
                    self.hitbox.right = self.hitbox.left
                if self.dir.x < 0: # moving left
                    self.hitbox.left = self.hitbox.right

        if direction == "vert":
            if self.hitbox.colliderect(self.target_pos):
                self.player.healthpoints -= 1
                if self.player.healthpoints <= 0:
                    self.player.playerstates = "dying"
                else:
                    self.player.playerstates = "hit"
                self.player.echo_hearts += 1
                self.player.player_time = pygame.time.get_ticks()
                if self.dir.y > 0: # moving down
                    self.hitbox.bottom = self.hitbox.top
                if self.dir.y < 0: # moving up
                    self.hitbox.top = self.hitbox.bottom

    def enemy_animation_tracker(self):
        if self.animation_state == "run_right":
            self.current_frame += 0.1
            if self.current_frame >= len(self.enemy_run_left):
                self.current_frame = 0
            self.image = self.enemy_run_right[int(self.current_frame)]            

        if self.animation_state == "run_left": 
            self.current_frame += 0.1
            if self.current_frame >= len(self.enemy_run_right):
                self.current_frame = 0
            self.image = self.enemy_run_left[int(self.current_frame)]            

        if self.state == "hit":
            pygame.transform.invert(self.image, self.image)

    def update(self):
        if self.player.playerstates != "recovering":
            self.chase()
            self.move(self.speed)        

        self.enemy_animation_tracker()
            # print("be inverted")
        # if self.state == "chase":
        #     print("Chasing")
        #     self.image = pygame.image.load("assets/Vegaslarge.png")
