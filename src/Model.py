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


    def main_loop(self):
        while True:
            if self.level.state == "game":
                self.game_loop()
            elif self.level.state == "reset":
                print("Re?")
                self.reset_loop()
            elif self.level.state == "menu":
                self.menu_loop()
            elif self.level.state == "exit":
                self.exit_loop()

    def game_loop(self):
        while self.level.state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level.state = "exit"
            if self.level.state == "game":
                self.screen.fill("black")
                self.level.render()
                pygame.display.update()
                self.clock.tick(FPS)
            if self.level.state == "reset":
                break

    def reset_loop(self):
        while self.level.state == "reset":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level.state = "exit"
            self.level.reset()

    def menu_loop(self):
        pass

    def exit_loop(self):
        pygame.quit()
        sys.exit()
