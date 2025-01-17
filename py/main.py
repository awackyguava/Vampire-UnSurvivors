from settings import *
from player import Player

class Game:
    def __init__(self):
        ## SETUP ##
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire UnSurvivors')
        self.clock = pygame.time.Clock()
        self.running = True

        ## Groups ##
        self.all_sprites = pygame.sprite.Group()
        
        ## Player ##
        self.player = Player((400,300), 1, 1, self.all_sprites)
    
    def exe(self):
        while self.running:
            ## dt ##
            dt = pygame.time.get_ticks() / 1000

            ## loop ## 
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False

            ## update ##
            self.all_sprites.update(dt)
            

            ## draw ##
            self.all_sprites.draw(self.window)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.exe()
