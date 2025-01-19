from settings import *
from player import Player
from sprites import *
from random import choice
from pytmx.util_pygame import load_pygame
from groups import *

class Game:
    def __init__(self):
        ## SETUP ##
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire UnSurvivors')
        self.clock = pygame.time.Clock()
        self.running = True

        ## Sheets ##
        self.player_sheet = pygame.image.load(join('images', 'rogues.png')).convert_alpha()
        self.weapon_sheet = pygame.image.load(join('images', 'items.png')).convert_alpha()
        self.enemy_sheet = pygame.image.load(join('images', 'monsters.png')).convert_alpha()

        ## Groups ##
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        ## Import Map ##
        self.map_setup()
        
        ## Sprites ##
        self.spawn_player(self.spawns)
    
    def map_setup(self):
        map = load_pygame(join('data', 'levels', 'level1.tmx'))
        self.spawns = [obj for obj in map.get_layer_by_name('Geometry') if obj.name == 'spawn']

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

    def spawn_player(self, spawn_points):
        spawn_point = choice(spawn_points)
        self.player = Player((spawn_point.x, spawn_point.y), self.getSprite(2,0,self.player_sheet), self.all_sprites, self.collision_sprites)
        self.player_weapon = Weapon(self.player, self.getSprite(2, 9, self.weapon_sheet), self.all_sprites)
        for i in range(6):
            Enemy(self.getSprite(0, 0, self.enemy_sheet), self.player, self.all_sprites, self.collision_sprites)

    def getSprite(self, sheet_x, sheet_y, sheet):
        ## Gets sprite from sprite sheet ##
        sheet_width = 32
        sheet_height = 32
        sheet_x *= sheet_width
        sheet_y *= sheet_height
        sprite = sheet.subsurface([sheet_x, sheet_y, sheet_width, sheet_height])
        return sprite

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
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.exe()
