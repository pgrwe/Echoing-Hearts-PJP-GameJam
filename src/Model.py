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

    def game_loop(self):
        while self.level.state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.render()
            # self.level.cursor_display()
            pygame.display.update()
            self.clock.tick(FPS)

    def reset_loop(self):
        while self.level.state == "reset":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.level.reset()

    def menu_loop(self):
        pass
    # def run(self):
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             if self.level.state == "reset":
    #                 new = self.game_loop()
    #             if self.level.state == "game":
    #                 current_loop = self.game_loop()
