import pygame, math, random
from src.Settings import *

class Player(pygame.sprite.Sprite):
    # def __init__(self, pos, groups, obj_sprites, create_spell):
    def __init__(self, pos, groups, obj_sprites):
        super().__init__(groups)
        # importing animation
        self.idle_right = []
        self.idle_right.append(pygame.image.load("assets/echomage/idle1_right.png"))
        self.idle_right.append(pygame.image.load("assets/echomage/idle2_right.png"))
        self.idle_right.append(pygame.image.load("assets/echomage/idle3_right.png"))

        self.idle_left = []
        self.idle_left.append(pygame.transform.flip(self.idle_right[0], True, False))
        self.idle_left.append(pygame.transform.flip(self.idle_right[1], True, False))
        self.idle_left.append(pygame.transform.flip(self.idle_right[2], True, False))

        self.run_right_list = []
        self.run_right_list.append(pygame.image.load("assets/echomage/run1_right.png"))
        self.run_right_list.append(pygame.image.load("assets/echomage/run2_right.png"))
        self.run_right_list.append(pygame.image.load("assets/echomage/run3_right.png"))
        self.run_right_list.append(pygame.image.load("assets/echomage/run4_right.png"))
        self.run_right_list.append(pygame.image.load("assets/echomage/run5_right.png"))

        self.run_left_list = []
        self.run_left_list.append(pygame.transform.flip(self.run_right_list[0], True, False))
        self.run_left_list.append(pygame.transform.flip(self.run_right_list[1], True, False))
        self.run_left_list.append(pygame.transform.flip(self.run_right_list[2], True, False))
        self.run_left_list.append(pygame.transform.flip(self.run_right_list[3], True, False))
        self.run_left_list.append(pygame.transform.flip(self.run_right_list[4], True, False))

        # animations
        self.current_frame = 0
        self.animation_state = "idle_right"

        self.image = self.idle_right[self.current_frame]

        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 8
        self.hitbox  = self.rect.inflate(-6,-10) # removes 3 px from left/right and 5 from top/bottom

        self.obj_sprites = obj_sprites

        # spell cooldown
        self.cooldown = 30

        # player resources
        self.playerstates = "alive"
        self.spell_cast = False
        # self.create_spell = create_spell
        self.healthpoints = 1
        self.echo_hearts = 0
        self.player_time = 0
        self.facing = "right"



    def input(self):
        # gets input keys to determine direction
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dir.y = -1
            if self.facing == "right" and self.dir.x == 0:
                self.animation_state = "run_right"
            elif self.facing == "left" and self.dir.x == 0:
                self.animation_state = "run_left"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dir.y = 1
            if self.facing == "right" and self.dir.x == 0:
                self.animation_state = "run_right"
            elif self.facing == "left" and self.dir.x == 0:
                self.animation_state = "run_left"
        else:
            self.dir.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dir.x = 1
            self.facing = "right"
            self.animation_state = "run_right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dir.x = -1
            self.facing = "left"
            self.animation_state = "run_left"
        else:
            self.dir.x = 0


        if self.facing == "right" and self.dir == (0,0):
            self.animation_state = "idle_right"
        elif self.facing == "left" and self.dir == (0,0):
            self.animation_state = "idle_left"

        # gets mouse input to determine spellcasts
        self.spell_timer = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and self.cooldown <= 0:
            self.spell_cast = True
            self.cooldown = 25

        self.cooldown-=1

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


    def state_tracker(self):
        if self.playerstates == "recovering":
            if pygame.time.get_ticks() - self.player_time > 1000:
                self.playerstates = "alive"

    def animation_tracker(self):
        if self.animation_state == "idle_right":
            self.current_frame += 0.1
            if self.current_frame >= len(self.idle_right):
                self.current_frame = 0
            self.image = self.idle_right[int(self.current_frame)]

        if self.animation_state == "idle_left":
            self.current_frame += 0.1
            if self.current_frame >= len(self.idle_left):
                self.current_frame = 0
            self.image = self.idle_left[int(self.current_frame)]

        if self.animation_state == "run_right":
            self.current_frame += 0.2
            if self.current_frame >= len(self.run_right_list):
                self.current_frame = 0
            self.image = self.run_right_list[int(self.current_frame)]

        if self.animation_state == "run_left":
            self.current_frame += 0.2
            if self.current_frame >= len(self.run_left_list):
                self.current_frame = 0
            self.image = self.run_left_list[int(self.current_frame)]

    def update(self):
        # print(self.healthpoints)
        # print(self.playerstates)
        self.state_tracker()
        self.animation_tracker()
        self.input()
        self.move(self.speed)



class Spell(pygame.sprite.Sprite):
    # def __init__(self,player,groups,mousepos):
    def __init__(self, player_rect, groups, mousepos, enemy_group):
        super().__init__(groups)
        # load in spell image later self.image = pygame.image.load().convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((25,25))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = player_rect.center)
        self.speed = 15
        self.spell_kill_timer = pygame.time.get_ticks()
        self.enemy_group = enemy_group
        self.enemy_timer = 500

        self.x_mouse, self.y_mouse = mousepos
        # how ever far the mouse is from the actual center is how far the mouse is from the player
        self.diff_x = self.x_mouse - 640
        self.diff_y = self.y_mouse - 360
        self.now_x_mouse = self.rect.x + self.diff_x
        self.now_y_mouse = self.rect.y + self.diff_y
        self.angle = math.atan2(self.now_y_mouse - self.rect.y, self.now_x_mouse - self.rect.x)

        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def spellsling(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.hit()

    def hit(self):
        for enemy in self.enemy_group:
            if self.rect.colliderect(enemy.hitbox):
                # print("E_hp: ", enemy.healthpoints)
                enemy.state = "hit"
                enemy.healthpoints -= 1
                self.enemy_timer -= 1

            # enemy.state = "chase"



    def update(self):
        # self.spell_cast()
        for enemy in self.enemy_group:
            if enemy.healthpoints <= 0:
                self.enemy_group.remove(enemy)
                enemy.kill()
        self.spellsling()
        if pygame.time.get_ticks() >= self.spell_kill_timer + 1000:
            self.kill()

class Echoes(pygame.sprite.Sprite):
    def __init__(self, player, groups, obj_sprites, enemy_group):
        super().__init__(groups)

        self.echo_idle_right = []
        self.echo_idle_right.append(pygame.image.load("assets/echomage/echo1_right.png"))
        self.echo_idle_right.append(pygame.image.load("assets/echomage/echo2_right.png"))
        self.echo_idle_right.append(pygame.image.load("assets/echomage/echo3_right.png"))

        self.echo_idle_left = []
        self.echo_idle_left.append(pygame.transform.flip(self.echo_idle_right[0], True, False))
        self.echo_idle_left.append(pygame.transform.flip(self.echo_idle_right[1], True, False))
        self.echo_idle_left.append(pygame.transform.flip(self.echo_idle_right[2], True, False))

        self.current_frame = 0

        self.image = self.echo_idle_left[self.current_frame]
        self.rect = self.image.get_rect(center = player.rect.center)

        self.echo_timer = pygame.time.get_ticks()
        self.hitbox = self.rect.inflate(30,30) # shrink 5 px from top and bottom
        self.player = player

        self.facing = self.player.facing
        self.state = "wait"

        self.enemy_group = enemy_group

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print("CONSUME")
            if self.player.healthpoints >= 2:
                self.consume_echo()

    def animation_tracker(self):
        if self.facing == "right":
            self.current_frame += 0.1
            if self.current_frame >= len(self.echo_idle_right):
                self.current_frame = 0
            self.image = self.echo_idle_right[int(self.current_frame)]

        if self.facing == "left":
            self.current_frame += 0.1
            if self.current_frame >= len(self.echo_idle_left):
                self.current_frame = 0
            self.image = self.echo_idle_left[int(self.current_frame)]


    def consume_echo(self):
        self.player.echo_hearts -= 1
        self.state = "attacking"
        for enemy in self.enemy_group:
            if self.hitbox.colliderect(enemy.hitbox):
                # print("E_hp: ", enemy.healthpoints)
                enemy.state = "hit"
                enemy.healthpoints -= 100

        print("Gone")


    def update(self):
        self.input()
        for enemy in self.enemy_group:
            if enemy.healthpoints <= 0:
                self.enemy_group.remove(enemy)
                enemy.kill()
        self.animation_tracker()
