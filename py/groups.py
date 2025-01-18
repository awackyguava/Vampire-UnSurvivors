from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.window = pygame.display.get_surface()
        self.camera_position = pygame.Vector2()

    ## Overriding original draw method for camera ##
    def draw(self, target):
        self.camera_position.x = (target[0] - WINDOW_WIDTH / 2) * -1
        self.camera_position.y = (target[1] - WINDOW_HEIGHT / 2) * -1

        ## Sorting Sprites into lists ##
        tile_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        deco_sprites = [sprite for sprite in self if hasattr(sprite, 'deco')]
        other_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') and not hasattr(sprite, 'deco')]
            
        ## Sort sprites by their center y value for handling overlaps ##
        for layer in [tile_sprites, deco_sprites, other_sprites]: 
            for sprite in sorted(layer, key= lambda sprite: sprite.rect.centery):
                self.window.blit(sprite.image, sprite.rect.topleft + self.camera_position)
