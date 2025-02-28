from settings import *
from player import *
from sprite import *
from groups import *
from random import randint
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Квадралипсис")
        self.clock = pygame.time.Clock()
        self.running = True


        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = EnemySprites()


        self.hit = Sword((-140, -140),self.enemy_sprites)

        self.setup()


        self.player = Player((200, 200), self.all_sprites, self.collision_sprites, self.createHit, self.deleteHit)
        self.enemy = []
        self.enemyHp = []



    def UI(self):
        self.text_surface = self.font.render("HP: " + str(self.player.hp),1,'black')
        self.text_diractionX = self.font.render("DirectX" + str(self.player.direction),1 ,'black')
        self.text_acc = self.font.render("Acc "+str(self.player.acceleration),1,'black')
        self.display_surface.blit(self.text_surface, (10,10))
        self.display_surface.blit(self.text_diractionX, (10,40))
        self.display_surface.blit(self.text_acc, (10,70))

       

    def setup(self):
        self.font = pygame.font.Font(None, 30)
        map = load_pygame('map2.tmx')
        for x,y,image in map.get_layer_by_name('Map').tiles():
            Block((x*TILE_SIZE,y*TILE_SIZE), image, self.all_sprites)

        for obj in (map.get_layer_by_name('Wall')):
            Collision((obj.x,obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            Collision((obj.x,obj.y), obj.image, (self.all_sprites,self.collision_sprites))
            #print((obj.x,obj.y), obj.image)

        

        

    def get_damage(self, enemies):
        for enemy in enemies:
            
            if enemy.collisionWithPlayer() and not self.player.isDied():
                self.player.damage(enemy)
                enemy.stop()
                
            elif self.player.isDied():
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

            
                
    def createHit(self,pos):          
        self.hit = Sword(pos,self.enemy_sprites)

    def deleteHit(self):
        self.enemy_sprites.remove(self.hit)
        self.hit.rect.x, self.hit.rect.y = -140, -140
        
        
                
    
            


    def run(self):
        while self.running:
            dt = self.clock.tick(60)/1000
            mousex,mousey = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.enemy.append(Enemy((mousex + self.player.rect.x - WINDOW_WIDTH//2,mousey + self.player.rect.y - WINDOW_HEIGHT//2), (self.all_sprites, self.collision_sprites, self.enemy_sprites), self.player))
                    self.enemyHp.append(EnemyHp(self.enemy[-1],self.all_sprites))
                    
                    
                if event.type == pygame.KEYDOWN and self.player.isDied():
                    if event.key == pygame.K_r:
                        self.player = Player((200, 200), self.all_sprites, self.collision_sprites, self.createHit, self.deleteHit)
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
