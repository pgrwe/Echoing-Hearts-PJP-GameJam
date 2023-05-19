import pygame, sys
from src.Level import Level
from src.Settings import *

class GameModel:
    # model = main (in concept)
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Echoing Hearts')

        # level setup
        self.level = Level()

    def run(self):
        
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            

