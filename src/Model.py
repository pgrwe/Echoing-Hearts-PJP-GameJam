import pygame, sys

class GameModel:
    '''
    handles game loop
    deals with collisions
    
    '''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Echoing Hearts')

    def run(self):
        
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            pygame.display.update()
            self.clock.tick(60)
            

