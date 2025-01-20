from settings import *

class Player(pygame.sprite.Sprite): ## TODO stats
    def __init__(self, pos, sprite, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.transform.scale2x(sprite)
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-15,-5)

        ## Vectors ##
        self.direction = pygame.Vector2()
        self.speed = 220

        ## Collisions ##
        self.collision_sprites = collision_sprites
    
    def keys(self):
        ## initalises keys, then sets and normalises direction vector ##
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) + int(keys[pygame.K_d]) - int(keys[pygame.K_LEFT]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN]) + int(keys[pygame.K_s]) - int(keys[pygame.K_UP]) - int(keys[pygame.K_w])
        if self.direction:
            self.direction = self.direction.normalize()
    
    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')

        self.hitbox.y += self.direction.y * self.speed * dt
        self.collisions('vertical')

        self.rect.center = self.hitbox.center

    def collisions(self, type):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                match type:
                    case 'horizontal':
                        ## if player moves into object, set its pos to the side it collided with ##
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
        self.keys()
        self.move(dt)
