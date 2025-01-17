from settings import *

## sheets ##
player_sheet = pygame.image.load(join('images', 'rogues.png'))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, s_x, s_y, *groups):
        super().__init__(*groups)
        self.image = self.getSprite(s_x, s_y)
        self.rect = self.image.get_frect(center = pos)

    def getSprite(self,s_x,s_y):
        s_width = 32
        s_height = 32
        s_x *= s_width
        s_y *= s_height
        sprite = player_sheet.subsurface([s_x, s_y, s_width, s_height])
        return sprite
    
    def move(self, dt):
        pass 
    
    def update(self, dt):
        pass
       