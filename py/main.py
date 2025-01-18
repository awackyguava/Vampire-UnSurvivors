from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame

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

        self.map_setup()
        
        ## Sprites ##
        self.player = Player((400,300), player_sheet, 2, 0, self.all_sprites, self.collision_sprites)
    
    def map_setup(self):
        map = load_pygame(join('data', 'levels', 'level1.tmx'))

        ## Tile Layer ##
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        ## Deco layer ##
        for x, y, image in map.get_layer_by_name('Deco').tiles():
            Deco((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        ## Geometry Layer ##
        for object in map.get_layer_by_name('Geometry'):
            if object.name == 'wall':
                Collision((object.x, object.y), pygame.Surface((object.width, object.height)), self.collision_sprites)

        ## Collidables Layer ##
        for object in map.get_layer_by_name('Collidables'):
            Collision((object.x, object.y), object.image, (self.all_sprites, self.collision_sprites))

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
