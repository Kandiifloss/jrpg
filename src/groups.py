from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)

        self.display = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -target_pos[0] + WINDOW_WIDTH / 2
        self.offset.y = -target_pos[1] + WINDOW_HEIGHT / 2
        for sprite in self:
            self.display.blit(sprite.image, sprite.rect.topleft + self.offset)


class EnemySprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
    
    def update(self, player, enemies):
        for enemy in enemies:
            enemy.player = player

