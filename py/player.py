from settings import *

## sheets ##
player_sheet = pygame.image.load(join('images', 'rogues.png'))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, s_x, s_y, groups, collison_sprites):
        super().__init__(groups)
        self.image = pygame.transform.scale_by(self.getSprite(s_x, s_y, player_sheet), 2)
        self.rect = self.image.get_frect(center = pos)

        ## Vectors ##
        self.direction = pygame.Vector2()
        self.speed = 500

        ## Collisions ##
        self.collison_sprites = collison_sprites

    def getSprite(self, s_x, s_y, sheet):
        ## Gets sprite from sprite sheet ##
        s_width = 32
        s_height = 32
        s_x *= s_width
        s_y *= s_height
        sprite = sheet.subsurface([s_x, s_y, s_width, s_height])
        return sprite
    
    def keys(self):
        ## initalises keys, then sets and normalises direction vector ##
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if self.direction:
            self.direction = self.direction.normalize()
    
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')

        self.rect.y += self.direction.y * self.speed * dt
        self.collisions('vertical')

    def collisions(self, type):
        for sprite in self.collison_sprites:
            if sprite.rect.colliderect(self.rect):
                match type:
                    case 'horizontal':
                        ## if player moves into object, set its pos to the side it collided with ##
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                        elif self.direction.x < 0:
                            self.rect.left = sprite.rect.right
                    case 'vertical':
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
    
    def update(self, dt):
        self.keys()
        self.move(dt)
       