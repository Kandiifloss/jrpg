from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, collision_sprites, createHit, deleteHit):
        super().__init__(groups)
        self.image = pygame.image.load("stone.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.hit_box = self.rect.inflate(-10,-10)
        self.collision_obj = collision_sprites
        self.type = 'player'
        
        self.sword = 0

        # cool down
        self.can_hit = True
        self.sword_timer = 0
        self.sword_cd = 400

        self.createHit = createHit
        self.deleteHit = deleteHit

        
        self.direction = pygame.Vector2()
        self.outDirection = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.speed = 500
        self.hp = 100
        self.attack = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        if keys[pygame.K_f] and self.can_hit:
            self.createHit((self.hit_box.x+5,self.hit_box.y+5))
            
            self.can_hit = False
            self.hit_time = pygame.time.get_ticks()

            
            


                


    def accelerationUpdate(self):
        if self.acceleration.x > 0: self.acceleration.x -= 1
        if self.acceleration.x < 0: self.acceleration.x += 1
        if self.acceleration.y > 0: self.acceleration.y -= 1
        if self.acceleration.y < 0: self.acceleration.y += 1
        if self.acceleration:
            self.direction.x = 0
            self.direction.y = 0
        
        



    def collision(self, direction):
        for obj in self.collision_obj:
            if self.hit_box.colliderect(obj.rect) and obj.type != 'enemy':
                if direction == 'horizontal':
                    if self.outDirection.x > 0: self.hit_box.right = obj.rect.left
                    if self.outDirection.x < 0: self.hit_box.left = obj.rect.right
                elif direction == 'vertical':
                    if self.outDirection.y < 0: self.hit_box.top = obj.rect.bottom
                    if self.outDirection.y > 0: self.hit_box.bottom = obj.rect.top
        
        
    def attackTimer(self):
        if not self.can_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= 1: self.deleteHit()
            if current_time - self.hit_time >= self.sword_cd:
                self.can_hit = True

                



        
        
                    
                


    def move(self,dt):
        self.accelerationUpdate()
        
        self.hit_box.x += self.direction.x * self.speed * dt + self.acceleration.x
        self.outDirection.x = self.direction.x + self.acceleration.x
        self.collision('horizontal')
        self.hit_box.y += self.direction.y * self.speed * dt + self.acceleration.y
        self.outDirection.y = self.direction.y + self.acceleration.y
        self.collision('vertical')
        self.rect.center = self.hit_box.center
    


    def damage(self, enemy):
        self.acceleration.x  = int(enemy.direction.x*10)
        self.acceleration.y = int(enemy.direction.y*10)
        self.rect.center = self.hit_box.center
        self.hp -= 10
        

    def isDied(self):
        if self.hp <= 0:
            self.direction.x = 0
            self.direction.y = 0
            self.acceleration = self.direction
            return True
        else:
            return False

        

    def update(self,dt):
        self.input()
        self.move(dt)
        self.attackTimer()
        

        



    def draw(self):
        pass
        




class Sword(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.Surface((200,200))
        #self.image.fill("black")
        self.rect = self.image.get_rect(center = pos)
        self.type = 'sword'

    






class EnemyHp(pygame.sprite.Sprite):
    def __init__(self, enemy, groups):
        super().__init__(groups)
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render(str(enemy.hp)+"/10",1,'black')
        self.enemy = enemy
        self.rect = enemy.image.get_rect(center = (enemy.rect.x, enemy.rect.y-10))

    def update(self, dt):
        self.rect = self.enemy.image.get_rect(center = (self.enemy.rect.x, self.enemy.rect.y-10))
        self.image = self.font.render(str(self.enemy.hp)+"/10",1,'black')
        



class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load('grass.png').convert()
        self.rect = self.image.get_rect(center = pos)
        self.type = 'enemy'
        self.player = player
        self.hp = 10

        self.speed = 100
        self.collision_obj = player.collision_obj
        self.direction = player.direction
        self.acceleration = pygame.Vector2()




        
        



    

    def collisionWithPlayer(self):
        if self.rect.colliderect(self.player.rect):
            return True

    def collision(self, direction):
        for obj in self.collision_obj:
            if self.rect.colliderect(obj.rect) and obj != self:
                if direction == 'horizontal':
                    if self.direction.x + self.acceleration.x > 0: self.rect.right = obj.rect.left                    
                    if self.direction.x + self.acceleration.x < 0: self.rect.left = obj.rect.right
                elif direction == 'vertical':
                    if self.direction.y + self.acceleration.y < 0: self.rect.top = obj.rect.bottom
                    if self.direction.y + self.acceleration.y > 0: self.rect.bottom = obj.rect.top
        

    def input(self):
        if self.player.hp >0:
            self.direction.x = self.player.rect.x - self.rect.x
            self.direction.y = self.player.rect.y - self.rect.y
            self.direction = self.direction.normalize() if self.direction else self.direction
        else:
            self.direction.x = 0
            self.direction.y = 0
        

    def stop(self):
        self.acceleration.x =  -int(self.direction.x*10)
        self.acceleration.y = -int(self.direction.y*10)

    def accelerationUpdate(self):
        if self.acceleration.x > 0: self.acceleration.x -= 1
        if self.acceleration.x < 0: self.acceleration.x += 1
        if self.acceleration.y > 0: self.acceleration.y -= 1
        if self.acceleration.y < 0: self.acceleration.y += 1
        if self.acceleration:
            self.direction.x = 0
            self.direction.y = 0

        



    

    def move(self,dt):
        self.accelerationUpdate()
        self.rect.x += self.direction.x * self.speed * dt + self.acceleration.x
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt + self.acceleration.y
        self.collision('vertical')
            



    def update(self, dt):
        self.move(dt)
        self.input()







        

        







        
        


    
        
