from pytmx.util_pygame import load_pygame
from random import randint
from settings import * #импорт констант?
import player 
import sprite 
import groups 
import pygame
#import pdb; pdb.set_trace()

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Квадралипсис')
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = groups.AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = groups.EnemySprites()

        self.setup()

        

        

    def UI(self):
        self.text_surface = self.font.render(f'HP: {self.player.hp}', 1, 'black')
        self.text_direction_x = self.font.render(f'DirectX {self.player.direction}', 1, 'black')
        self.text_acc = self.font.render(f'Acc {self.player.acceleration}', 1, 'black')
        self.display_surface.blit(self.text_surface, (10, 10))
        self.display_surface.blit(self.text_direction_x, (10, 40))
        self.display_surface.blit(self.text_acc, (10, 70))

    def setup(self):
        self.font = pygame.font.Font(None, 30)
        map = load_pygame('maps/map2.tmx')
        
        
        for x, y, image in map.get_layer_by_name('Map').tiles():
            sprite.Block((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in (map.get_layer_by_name('Wall')):
            sprite.Collision((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            sprite.Collision((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
            #print((obj.x,obj.y), obj.image)
        self.player = player.Player((200, 200), self.all_sprites, self.collision_sprites, self.enemy_sprites)
        for i in range(5):
            player.Enemy((randint(0,1000), randint(0, 2000)),(self.all_sprites, self.collision_sprites, self.enemy_sprites), self.player)
            
        for enemy in self.enemy_sprites:
            print(enemy.rect)
                
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    player.Enemy((mouse_x + self.player.rect.x - WINDOW_WIDTH // 2, mouse_y + self.player.rect.y - WINDOW_HEIGHT // 2), 
                                 (self.all_sprites, self.collision_sprites, self.enemy_sprites), self.player)
                    
                if event.type == pygame.KEYDOWN and self.player.hp <= 0:
                    if event.key == pygame.K_r:
                        self.player = player.Player((200, 200), self.all_sprites, self.collision_sprites, self.enemy_sprites)
                        self.player.hp = 100
                        print("Respawn")
                        self.enemy_sprites.update(self.player, self.enemy_sprites)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    for enemy in self.enemy_sprites:
                        print(enemy.rect)
            
            #update
                        
            self.all_sprites.update(dt=dt)

            
            
                    
            #draw
            self.display_surface.fill("white")
            self.all_sprites.draw(self.player.rect.center)
            self.UI()
            pygame.display.update()
        pygame.quit()

game = Game()
game.run()
