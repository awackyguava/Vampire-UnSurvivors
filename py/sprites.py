from settings import *
from random import choice, randint

class Collision(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class Deco(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft = pos)
        self.deco = True

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, sprite, groups):
        super().__init__(groups)

        ## Player ##
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(1,0)

        ## Setup ##
        self.weapon_surface = pygame.transform.scale2x(sprite)
        self.image = self.weapon_surface
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        player_position = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    def update(self, dt):
        self.get_direction()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance   

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite, player, groups, collision_sprites):
        super().__init__(groups)

        self.player = player

        self.image = pygame.transform.scale2x(sprite)
        self.rect = self.image.get_frect(center = self.get_spawn())
        self.hitbox = self.rect.inflate(-15, -5)

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()

    def get_spawn(self):

        player_pos = self.player.rect.center

        left_edge = int(player_pos[0] - WINDOW_WIDTH // 2)
        right_edge = int(player_pos[0] + WINDOW_WIDTH // 2)
        top_edge = int(player_pos[1] - WINDOW_HEIGHT // 2)
        bottom_edge = int(player_pos[1] + WINDOW_HEIGHT // 2)

        direction = choice(['top', 'bottom', 'left', 'right'])

        if direction == 'top':
            x = randint(left_edge - 100, right_edge + 100)
            y = top_edge - 100
        elif direction == 'bottom':
            x = randint(left_edge - 100, right_edge + 100)
            y = bottom_edge + 100
        elif direction == 'left':
            x = left_edge - 100
            y = randint(top_edge - 100, bottom_edge + 100)
        elif direction == 'right':
            x = right_edge + 100
            y = randint(top_edge - 100, bottom_edge + 100)

        return (x, y)
    
    # def update(self, dt):

            

        

