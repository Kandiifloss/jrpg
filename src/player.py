from settings import *
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, enemy_sprites):
        #Запихиваем сначала мечь в группу спрайтов, так что он первый рисуется. (временное решение, чтобы его не отображать, достаточно не вписывать мечь в all_sprites вовсе)
        self.sword = Sword((-140, -140), groups, enemy_sprites)
        super().__init__(groups)
        self.image = pygame.image.load('images/stone.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hit_box = self.rect.inflate(-10, -10)
        self.collision_obj = collision_sprites
        self.type = 'player'
        
        #self.sword = Sword((-140, -140), groups, enemy_sprites)

        # cool down
        self.can_hit = True
        self.sword_timer = 0
        self.sword_cd = 400

        self.direction = pygame.Vector2()
        self.out_direction = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.speed = 200
        self.hp = 100
        self.attack = 0
        self.face = pygame.Vector2()

    def kill(self):
        super().kill()
        self.sword.kill()

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        #короче записываем крайний вектор
        if self.direction != (0,0) and self.face != self.direction:
            self.face = self.direction 
        #короче рисуем перед лицом вектор*расстояние
        if keys[pygame.K_f] and self.can_hit:
            self.sword.hit((self.face.x*50 + self.rect.centerx, self.face.y*50 + self.rect.centery))
            
            self.can_hit = False
            self.hit_time = pygame.time.get_ticks()

    def acceleration_update(self):
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
                    if self.out_direction.x > 0: self.hit_box.right = obj.rect.left
                    if self.out_direction.x < 0: self.hit_box.left = obj.rect.right
                elif direction == 'vertical':
                    if self.out_direction.y < 0: self.hit_box.top = obj.rect.bottom
                    if self.out_direction.y > 0: self.hit_box.bottom = obj.rect.top
        
    def attack_timer(self):
        if not self.can_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.sword_cd:
                self.can_hit = True

    def move(self, dt):
        self.acceleration_update()
        
        self.hit_box.x += self.direction.x * self.speed * dt + self.acceleration.x
        self.out_direction.x = self.direction.x + self.acceleration.x
        self.collision('horizontal')
        self.hit_box.y += self.direction.y * self.speed * dt + self.acceleration.y
        self.out_direction.y = self.direction.y + self.acceleration.y
        self.collision('vertical')
        self.rect.center = self.hit_box.center

    def get_hit(self, enemy):
        self.acceleration.x  = int(enemy.direction.x * 20)
        self.acceleration.y = int(enemy.direction.y * 20)
        self.rect.center = self.hit_box.center
        self.hp -= enemy.damage
        if self.hp <= 0:
            self.kill()

    def update(self, **kwargs):
        self.input()
        self.move(kwargs['dt'])
        self.attack_timer()


class Sword(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.fill('brown')
        self.rect.center = pos
        self.enemy_sprites = enemy_sprites
        self.type = 'sword'
        self.damage = 1

    def hit(self, pos):
        self.rect.center = pos
        for enemy in self.enemy_sprites:
            if self.rect.colliderect(enemy.rect):
                enemy.get_hit(self.damage)
                enemy.stop()

    



class EnemyHp(pygame.sprite.Sprite):
    def __init__(self, enemy, groups):
        super().__init__(groups)
        self.font = pygame.font.Font(None, 30)
        self.enemy = enemy

    def update(self, **kwargs):
        self.rect = self.enemy.image.get_rect(center=(self.enemy.rect.x, self.enemy.rect.y - 10))
        self.image = self.font.render(f'{self.enemy.hp}/{self.enemy.max_hp}', 1, 'black')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load('images/grass.png').convert()
        self.rect = self.image.get_rect(center=pos)
        self.type = 'enemy'
        self.player = player
        self.max_hp = self.hp = 5
        self.damage = 10
        self.hp_surface = EnemyHp(self, groups[0])

        self.speed = 100
        self.collision_obj = player.collision_obj
        self.direction = player.direction
        self.acceleration = pygame.Vector2()

    def kill(self):
        super().kill()
        self.hp_surface.kill()

    def get_hit(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            self.kill()

    def collision_with_player(self):
        return self.rect.colliderect(self.player.rect)

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
        if self.player.hp > 0:
            self.direction.x = self.player.rect.x - self.rect.x
            self.direction.y = self.player.rect.y - self.rect.y
            self.direction = self.direction.normalize() if self.direction else self.direction
        else:
            self.direction.x = 0
            self.direction.y = 0

    def stop(self):
        self.acceleration.x = -int(self.direction.x * 20)
        self.acceleration.y = -int(self.direction.y * 20)

    def acceleration_update(self):
        if self.acceleration.x > 0: self.acceleration.x -= 1
        if self.acceleration.x < 0: self.acceleration.x += 1
        if self.acceleration.y > 0: self.acceleration.y -= 1
        if self.acceleration.y < 0: self.acceleration.y += 1
        if self.acceleration:
            self.direction.x = 0
            self.direction.y = 0

    def move(self, dt):
        self.acceleration_update()
        self.rect.x += self.direction.x * self.speed * dt + self.acceleration.x
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt + self.acceleration.y
        self.collision('vertical')
        if self.collision_with_player():
            self.player.get_hit(self)
            self.stop()

    def update(self, **kwargs):
        self.input()
        self.move(kwargs['dt'])
