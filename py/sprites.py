from settings import *
from random import choice, randint
from math import hypot, atan2, degrees

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
    def __init__(self, player, sprite, groups, enemy_sprites):
        super().__init__(groups)

        ## Player ##
        self.player = player
        self.distance = 50
        self.player_direction = pygame.Vector2(1,0)

        ## Setup ##
        self.weapon_surface = pygame.transform.scale2x(sprite)
        self.image = self.weapon_surface
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

        self.enemy_sprites = enemy_sprites

    def find_closest(self, player, enemies):
        closest_enemy = None
        smallest_distance = float(10000)

        if not enemies:
            return None

        ## Loop through each enemy to calculate distances ##
        for enemy in enemies:
            distance = hypot(player[0] - enemy[0], player[1] - enemy[1])
            if distance < smallest_distance:
                smallest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def get_direction(self):
        player_position = pygame.Vector2(self.player.rect.center)

        enemy_positions = [enemy.rect.center for enemy in self.enemy_sprites]

        cloest_enemy = self.find_closest(player_position, enemy_positions)

        if cloest_enemy:
            player_direction = (pygame.Vector2(cloest_enemy) - player_position)
            if player_direction:
                self.player_direction = player_direction.normalize()
    
    def rotate(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) + 45
        self.image = pygame.transform.rotozoom(self.weapon_surface, angle, 1)

    def update(self, dt):
        self.get_direction()
        self.rotate()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        self.shoot(dt)

class Enemy(pygame.sprite.Sprite): ## TODO make a parent for this and player
    def __init__(self, sprite, player, groups, collision_sprites, map):
        super().__init__(groups)

        self.player = player

        self.og_image = pygame.transform.scale2x(sprite)
        self.image = self.og_image
        self.rect = self.image.get_frect(center = self.get_spawn(map))
        self.hitbox = self.rect.inflate(-15, -5)

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 150

        ## Timer ## 
        self.death_start = 0
        self.death_duration = 400


    def get_spawn(self, map):

        player_pos = self.player.rect.center

        left_edge = int(player_pos[0] - WINDOW_WIDTH // 2) - 100
        right_edge = int(player_pos[0] + WINDOW_WIDTH // 2) + 100
        top_edge = int(player_pos[1] - WINDOW_HEIGHT // 2) - 100
        bottom_edge = int(player_pos[1] + WINDOW_HEIGHT // 2) + 100

        while True:
            direction = choice(['top', 'bottom', 'left', 'right'])

            if direction == 'top':
                x = randint(left_edge, right_edge)
                y = top_edge
            elif direction == 'bottom':
                x = randint(left_edge, right_edge)
                y = bottom_edge
            elif direction == 'left':
                x = left_edge
                y = randint(top_edge, bottom_edge)
            elif direction == 'right':
                x = right_edge
                y = randint(top_edge, bottom_edge)
            
            if (x > 0 and x < map.width * TILE_SIZE) and (y > 0 and y < map.height * TILE_SIZE):
                return (x,y)

    def move(self, dt):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        self.hitbox.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collisions('vertical')

        self.rect.center = self.hitbox.center

    def die(self):
        self.death_start = pygame.time.get_ticks()

        hurt = pygame.Surface(self.image.size).convert_alpha()
        hurt.fill('red')

        self.image.blit(hurt, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

    def dead_timer(self):
        if pygame.time.get_ticks() - self.death_start >= self.death_duration:
            self.kill()

    def collisions(self, type):
        ## Same as one in player ##
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                match type:
                    case 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.rect.left
                        elif self.direction.x < 0:
                            self.hitbox.left = sprite.rect.right
                    case 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.rect.top
                        elif self.direction.y < 0:
                            self.hitbox.top = sprite.rect.bottom
        
    def update(self, dt):
        if self.death_start == 0:
            self.move(dt)
        else:
            self.dead_timer()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprite, pos, direction, groups):
        super().__init__(groups)

        self.image = pygame.transform.rotozoom(sprite, degrees(atan2(direction.x, direction.y)) - 225, 1)
        self.rect = self.image.get_frect(midtop = pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = 1000

        ## lifetime stuff ##
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()


