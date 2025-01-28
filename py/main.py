from settings import *
from sprites import *
from random import choice
from pytmx.util_pygame import load_pygame
from groups import *
from ui import UI
from stats import Stats

class Game: ## TODO menus, loading + saving data
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
        self.projectile_sprites = pygame.sprite.Group()

        ## Import Map ##
        self.map = self.map_setup()
        
        ## Characters ##
        self.character_stats = {
            'archer' : Stats(150, 30, 250),
            'knight' : Stats(200, 20, 200),
            'mage' : Stats(100, 40, 225),
        }
        self.character_sprites = {
            'archer' : (2, 0, self.player_sheet),
            'knight' : (2, 1, self.player_sheet),
            'mage' : (1, 4, self.player_sheet),
        }

        self.player_spawned = False

        ## Timers ##
        self.timer_start = 0
        self.difficulty_start = 0

        self.enemy_spawn = pygame.event.custom_type()
        self.rate = 2000
        pygame.time.set_timer(self.enemy_spawn, self.rate)

        self.shoot = pygame.event.custom_type()
        pygame.time.set_timer(self.shoot, 700)

        ## Audio ##
        self.bg_music = pygame.mixer.Sound(join('data', 'Music', 'electo_bg.mp3'))
        self.bg_music.set_volume(0.3)
        self.bg_music.play(-1)

        self.game_music = pygame.mixer.Sound(join('data', 'Music', 'rock_bg.mp3'))
        self.game_music.set_volume(0.3)

        self.current_music = 'bg'

        ## Text ##
        self.timer_text = pygame.font.Font(join('data', 'Fonts', 'Cormorant','Cormorant-VariableFont_wght.ttf'), 50)

        ## UI ##
        self.ui = UI()

        ## State ##
        self.state = 'start_menu'

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
        
        return map

    def spawn_player(self, spawn_points, character):
        stats = self.character_stats[character]
        x, y, sheet = self.character_sprites[character]
        sprite = self.getSprite(x, y, sheet)
        spawn_point = choice(spawn_points)
        self.player = Player((spawn_point.x, spawn_point.y), sprite, self.all_sprites, self.collision_sprites, stats)
        self.player_weapon = Weapon(self.player, self.getSprite(2, 9, self.weapon_sheet), self.all_sprites, self.enemy_sprites)

    def getSprite(self, sheet_x, sheet_y, sheet):
        ## Gets sprite from sprite sheet ##
        sheet_width = 32
        sheet_height = 32
        sheet_x *= sheet_width
        sheet_y *= sheet_height
        sprite = sheet.subsurface([sheet_x, sheet_y, sheet_width, sheet_height])
        return sprite

    def projectile_collision(self):
        if self.projectile_sprites:
            for proj in self.projectile_sprites:
                collided_sprites = pygame.sprite.spritecollide(proj, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collided_sprites:
                    for sprite in collided_sprites:
                        sprite.die()
    
    def player_collision(self):
        collided_enemies = pygame.sprite.spritecollide(
            self.player, self.enemy_sprites, False, pygame.sprite.collide_mask
        )

        for enemy in collided_enemies:
            if enemy.death_start == 0:
                self.running = False

    def spawn_rate(self): ## TODO change into wave function, different minutes different waves etc
        difficulty_timer = self.time - self.difficulty_start
        if self.rate > 200 and difficulty_timer >= 10:
            pygame.time.set_timer(self.enemy_spawn, self.rate)
            self.rate -= 100
            self.difficulty_start = self.time

    def exe(self):
        while self.running:
            ## dt ##
            dt = self.clock.tick() / 1000
            self.time = pygame.time.get_ticks() / 1000

            ## loop ## 
            for event in pygame.event.get():
                match self.ui.state:
                    case 'start_menu':
                        if event.type == pygame.QUIT:
                                self.running = False
                    
                    case 'start':
                        if event.type == pygame.QUIT:
                            self.running = False

                    case 'start_game':
                            if self.timer_start == 0:
                                self.timer_start = self.time
                                self.difficulty_start = self.time

                            if self.current_music != 'game':    
                                self.bg_music.stop()
                                self.game_music.play(-1)
                                self.current_music = 'game'
                            
                            match event.type:
                                case pygame.QUIT:
                                    self.running = False

                                case self.enemy_spawn:
                                    Enemy(
                                        self.getSprite(0, 0, self.enemy_sheet),
                                        self.player, 
                                        (self.all_sprites, self.enemy_sprites), 
                                        self.collision_sprites,
                                        self.map,
                                        Stats(100,10,150)
                                        )
                                    Enemy(
                                        self.getSprite(1, 10, self.enemy_sheet),
                                        self.player, 
                                        (self.all_sprites, self.enemy_sprites), 
                                        self.collision_sprites,
                                        self.map,
                                        Stats(100,10,150)
                                        )
                                    Enemy(
                                        self.getSprite(1, 10, self.enemy_sheet),
                                        self.player, 
                                        (self.all_sprites, self.enemy_sprites), 
                                        self.collision_sprites,
                                        self.map,
                                        Stats(100,10,150)
                                        )
                                     
                                case self.shoot:
                                    if self.player_weapon.can_shoot():
                                        Projectile(
                                            self.getSprite(0, 6, self.weapon_sheet),
                                            self.player_weapon.rect.center,
                                            self.player_weapon.player_direction,
                                            (self.all_sprites, self.projectile_sprites),
                                        )
                            
            ## Menu ##
            if self.ui.state == 'start_menu':
                self.ui.update()
                self.ui.draw()

            elif self.ui.state == 'start':
                self.ui.update()
                self.ui.draw()

            elif self.ui.state == 'start_game':
                ## Update ##
                if not self.player_spawned:
                    self.spawn_player(self.spawns, self.ui.selected_character)
                    self.player_spawned = True

                self.spawn_rate()
                self.all_sprites.update(dt)
                self.projectile_collision()
                self.player_collision()

                ## Draw ##
                self.window.fill('darkgreen')
                self.all_sprites.draw(self.player.rect.center)

                if self.timer_start > 0:
                    minutes, seconds = divmod(int(self.time - self.timer_start), 60)
                    text_surface = self.timer_text.render(f"{minutes:02}:{seconds:02}", True, 'white') 
                    self.window.blit(text_surface, (WINDOW_WIDTH / 2 - 30, 10))
            
            elif self.ui.state == 'quit':
                self.running = False

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.exe()
