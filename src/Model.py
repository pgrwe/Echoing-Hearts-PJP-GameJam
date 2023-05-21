import pygame, sys
from src.Level import Level
from src.Settings import *

class GameModel:
    # model = main (in concept)
    def __init__(self):
        # general setup
        pygame.init()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Echoing Hearts')

        # level setup
        self.level = Level()

    def menu_loop(self):
        pass 

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.level.state == "game":
                self.screen.fill("black")
                self.level.render()
                pygame.display.update()
                self.clock.tick(FPS)
            if self.level.state == "reset":
                break

    def run(self):
        self.game_loop()


