from settings import *
from player import Player
from sprites import *
from random import randint

class Game:
    def __init__(self):
        ## SETUP ##
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire UnSurvivors')
        self.clock = pygame.time.Clock()
        self.running = True

        ## Sheets ##
        player_sheet = pygame.image.load(join('images', 'rogues.png')).convert_alpha()

        ## Groups ##
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        ## Sprites ##
        self.player = Player((400,300), player_sheet, 2, 0, self.all_sprites, self.collision_sprites)
        for i in range(6):
            Collision((randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)), (randint(60,100),randint(40,80)), (self.all_sprites,self.collision_sprites))
    
    def exe(self):
        while self.running:
            ## dt ##
            dt = self.clock.tick() / 1000

            ## loop ## 
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False

            ## update ##
            self.all_sprites.update(dt)
            

            ## draw ##
            self.window.fill('darkgray')
            self.all_sprites.draw(self.window)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.exe()
