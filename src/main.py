from pytmx.util_pygame import load_pygame
from random import randint
from settings import * #импорт констант?
import player 
import sprite 
import groups 
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Квадралипсис")
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = groups.AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = groups.EnemySprites()

        self.hit = player.Sword((-140, -140), self.enemy_sprites)

        self.setup()

        self.player = player.Player((200, 200), self.all_sprites, self.collision_sprites, self.create_hit, self.delete_hit)
        self.enemy = []
        self.enemyHp = []

    def UI(self):
        self.text_surface = self.font.render("HP: " + str(self.player.hp), 1, 'black')
        self.text_direction_x = self.font.render("DirectX" + str(self.player.direction), 1, 'black')
        self.text_acc = self.font.render("Acc " + str(self.player.acceleration), 1, 'black')
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

    def get_damage(self, enemies):
        for enemy in enemies:
            if enemy.collision_with_player() and not self.player.is_died():
                self.player.damage(enemy)
                enemy.stop()
            elif self.player.is_died():
                self.all_sprites.remove(self.player)
                self.player.rect

            if enemy.hp <= 0:
                self.all_sprites.remove(enemy)
                self.collision_sprites.remove(enemy)
                self.enemy_sprites.remove(enemy)
                enemies.remove(enemy)
                
            if enemy.rect.colliderect(self.hit.rect):
                enemy.hp -= 1
                print(enemy.hp)
                enemy.stop()
                
    def create_hit(self, pos):          
        self.hit = player.Sword(pos, self.enemy_sprites)

    def delete_hit(self):
        self.enemy_sprites.remove(self.hit)
        self.hit.rect.x, self.hit.rect.y = -140, -140

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.enemy.append(player.Enemy((mouse_x + self.player.rect.x - WINDOW_WIDTH // 2, mouse_y + self.player.rect.y - WINDOW_HEIGHT // 2), 
                                                  (self.all_sprites, self.collision_sprites, self.enemy_sprites), self.player))
                    self.enemyHp.append(player.EnemyHp(self.enemy[-1], self.all_sprites))
                    
                if event.type == pygame.KEYDOWN and self.player.is_died():
                    if event.key == pygame.K_r:
                        self.player = player.Player((200, 200), self.all_sprites, self.collision_sprites, self.create_hit, self.delete_hit)
                        self.player.hp = 100
                        print("Respawn")
                        self.enemy_sprites.update(self.player, self.enemy)
            
            #update
            self.all_sprites.update(dt)
            self.get_damage(self.enemy)
                    
            #draw
            self.display_surface.fill("white")
            self.all_sprites.draw(self.player.rect.center)
            self.UI()
            pygame.display.update()
        pygame.quit()

game = Game()
game.run()

