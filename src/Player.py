import pygame, math, random
from src.Settings import *

class Player(pygame.sprite.Sprite):
    # def __init__(self, pos, groups, obj_sprites, create_spell):
    def __init__(self, pos, groups, obj_sprites):
        super().__init__(groups)
        # importing animation
        self.idle_list = []
        self.idle_list.append(pygame.image.load("assets/echomage/idle1_right.png"))
        self.idle_list.append(pygame.image.load("assets/echomage/idle2_right.png"))
        self.idle_list.append(pygame.image.load("assets/echomage/idle3_right.png"))
        # animations
        self.current_frame = 0
        self.is_animating = False

        self.image = self.idle_list[self.current_frame]

        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.speed = 8
        self.hitbox  = self.rect.inflate(-6,-10) # removes 3 px from left/right and 5 from top/bottom

        self.obj_sprites = obj_sprites

        # spell cooldown
        self.cooldown = 300

        # player resources
        self.playerstates = "alive"
        self.spell_cast = False
        # self.create_spell = create_spell
        self.healthpoints = 1
        self.player_time = 0



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
            self.animate()
            self.spell_cast = True

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

    def animate(self):
        self.is_animating = True

    def state_tracker(self):
        if self.playerstates == "recovering":
            if pygame.time.get_ticks() - self.player_time > 1000:
                self.playerstates = "alive"

    def update(self):
        print(self.healthpoints)
        print(self.playerstates)
        if self.is_animating == True:
            self.current_frame += 1

            if self.current_frame >= len(self.idle_list):
                self.current_frame = 0
            
            self.image = self.idle_list[self.current_frame]

        self.state_tracker()
        self.input()
        self.move(self.speed)



class Spell(pygame.sprite.Sprite):
    # def __init__(self,player,groups,mousepos):
    def __init__(self, player_rect, groups, mousepos):
        super().__init__(groups)
        # load in spell image later self.image = pygame.image.load().convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.Surface((10,10))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = player_rect.center)
        self.speed = 15
        self.spell_kill_timer = pygame.time.get_ticks()

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


    def update(self):
        # self.spell_cast()
        self.spellsling()
        if pygame.time.get_ticks() >= self.spell_kill_timer + 300:
            self.kill()

class Echoes(pygame.sprite.Sprite):
    def __init__(self, player, groups, obj_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((20,20))
        self.image.fill((150,20,87))
        self.rect = self.image.get_rect(center = player.rect.center)
        self.rect.x += random.randint(-10,10)
        self.rect.y += random.randint(-10,10)

        self.echo_timer = pygame.time.get_ticks()
        self.hitbox = self.rect.inflate(0,-10) # shrink 5 px from top and bottom
        self.player = player


    def consume_echo(self):
        # collsion stuff related to the ground or other objects (static)
        if pygame.time.get_ticks() >= self.echo_timer + 600:
            if self.player.hitbox.colliderect(self.hitbox):
                self.player.healthpoints += 1
                self.kill()

    def update(self):
        self.consume_echo()


