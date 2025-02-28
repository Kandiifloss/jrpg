import pygame
#import pdb; pdb.set_trace()
from random import randint
pygame.init()


width = 1200  #<>
length = 900 #^

screen = pygame.display.set_mode((width,length))
pygame.display.set_caption("Пьяный куб")
clock = pygame.time.Clock()
    
cellSize = 30
temp_x = cellSize
temp_y = cellSize

world = []
worldWidth, worldHeigth = width//cellSize + 1, length//cellSize + 1
try:
    file = open('map.txt', 'r')
    row, col = 0,0
    line2 = []
    for line in file:
        for s in line:
            line2.append(int(s))
            col += 1
            if col >= worldWidth:
                world.append(line2)
                line2 = []
                row += 1
                col = 0
    file.close()
    print("loaded")
except:
    print("файл не найден")


class Player:
    def __init__(self, px, py, color, keyList):
        objects.append(self)
        self.type = 'player'
        self.x = px
        self.y = py
        self.color = color

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        

        self.rect = pygame.Rect(px,py, cellSize-5, cellSize-5)
        self.speed = 200

    

    

    def update(self):
        oldx,oldy = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.speed*dt
        if keys[self.keyRIGHT]:
            self.rect.x += self.speed*dt
        if keys[self.keyUP]:
            self.rect.y -= self.speed*dt
        if keys[self.keyDOWN]:
            self.rect.y += self.speed*dt

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect) and obj.type == 'block':
                if obj.id == 1:
                    self.rect.x = oldx
                    self.rect.y = oldy
            if obj != self and self.rect.colliderect(obj.rect) and obj.type == 'enemy':
                self.rect.x = oldx
                self.rect.y = oldy
                obj.hp -= 1
                
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 1)


class Enemy:
    def __init__(self, px,py,color):
        objects.append(self)
        self.type = 'enemy'
        self.x = px
        self.y = py
        self.color = color
        self.hp = 10

        self.rect = pygame.Rect(px-cellSize//2,py-cellSize//2, cellSize-5, cellSize-5)

    def update(self):
        if self.hp < 1:
            objects.remove(self)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 1)



class Block:
    def __init__(self, px, py, size, blockId):
        #blocks.append(self)
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px,py,size,size)
        self.id = blockId
        

    def update(self):
        pass
        

    def draw(self):
        #pygame.draw.rect(screen, 'white', self.rect, 1)
        if self.id == 1:
            screen.blit(stone, self.rect)
            #pygame.draw.rect(screen, 'white', self.rect, 1)
        elif self.id == 0:
            screen.blit(floor, self.rect)
            #pygame.draw.rect(screen, 'white', self.rect, 1)
            pass

        
floor = pygame.image.load("floor.png").convert()
stone = pygame.image.load("stone.png").convert()
font = pygame.font.Font(None, 50)
fps = 0
text_surface = font.render(str(fps), 1, 'white')


objects = []



def drawmap():
    for row in range(worldHeigth):
        for col in range(worldWidth):
            if world[row][col] == 1:
                Block(col*cellSize - cellSize//2 ,row*cellSize - cellSize//2 , cellSize, 1)
            elif world[row][col] == 0:
                Block(col*cellSize - cellSize//2 ,row*cellSize - cellSize//2 , cellSize, 0)
                

drawmap()                
Player (30,30, 'blue', (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s))
Enemy(60,60,'red')







player_timer = pygame.USEREVENT + 1
pygame.time.set_timer(player_timer, 250)


while True:
    dt = clock.tick(120)/1000
    #обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Enemy(mouseCol*cellSize, mouseRow*cellSize, 'red')
    keys = pygame.key.get_pressed()
    
    for obj in objects:
        obj.update()

        
    screen.fill("black")
    for obj in objects:
        obj.draw()

    


    #курсор блоковs
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseRow, mouseCol = (mouseY + cellSize//2)//cellSize, (mouseX + cellSize//2)//cellSize
    square = pygame.draw.rect(screen, "White", (mouseCol*cellSize - cellSize//2 ,mouseRow*cellSize - cellSize//2 , cellSize, cellSize),1)
    
    
    circle = pygame.draw.circle(screen,'black', (100, 100),50)

    
    
                    
    
    fps = int(clock.get_fps())
    text_surface = font.render(str(fps), 1, 'green')
    
    screen.blit(text_surface, (0,0))
            
          
    pygame.display.update()
