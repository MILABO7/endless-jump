import pygame
import random

pygame.init()
pygame.joystick.init()
sticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


screen = pygame.display.set_mode((600,800))
pygame.display.set_caption('Infinite Jump')

#setting frame rate
clock = pygame.time.Clock()
FPS = 60

#game var
GRAVITY = 1
MAX_FLOOR = 10
SCROLL_TRESH = 200
scroll = 0
gameOver = False
score = 0

#font
fontSmall = pygame.font.SysFont('Arial', 20)
fontBig = pygame.font.SysFont('Arial', 24)

#image load
playerImg = pygame.image.load('player.png').convert_alpha()
floorImg = pygame.image.load("floor.png").convert_alpha()
ground = pygame.image.load('ground.png').convert_alpha()


#player class
class Player():
    def __init__(self, x, y):
        self.image = playerImg
        self.rect = self.image.get_rect() #get the rectangle of player image
        self.rect.center = (x,y) #rect position
        self.vel_y = 0
        self.isJump = False

    def drawPlayer(self):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255,0,0), self.rect, 2)

    def move(self):
        y_change = 0
        scroll = 0
        #keyboard process
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
            if self.rect.x <= 0:
                self.rect.x = 580
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
            if self.rect.x >= 580:
                self.rect.x = 0
        #joystick process
        if len(sticks) >= 1:
            joystick = pygame.joystick.Joystick(0)
            joyX = joystick.get_axis(0)
            joyJump = joystick.get_button(0)
            if joyX > 0:
                self.rect.x += 10
                if self.rect.x >= 580:
                    self.rect.x = 0
            if joyX < 0:
                self.rect.x -= 10
                if self.rect.x <= 0:
                    self.rect.x = 580
        
        #gravity
        self.vel_y += GRAVITY
        y_change += self.vel_y
      
        #ground collision (needs cleaner code)
        if len(ground_group) == 1:
            if self.rect.bottom + y_change > ground.rect.y:
                y_change = 0
                self.vel_y = 0
                self.rect.bottom = ground.rect.top
                #jumping
                if key[pygame.K_SPACE]:
                    self.vel_y = -20
                if len(sticks) >= 1 and joyJump == True:
                    self.vel_y = -20
        else:
            if self.rect.top + y_change > 800:
                y_change = 0
                self.vel_y = 0
                self.rect.top = 800
                

        #floor collisions
        for floor in floor_group:
            if floor.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                #check if above floor
                if self.rect.bottom < floor.rect.centery:
                    if self.vel_y > 0:
                        y_change = 0
                        self.vel_y = 0
                        self.rect.bottom = floor.rect.top
                        if key[pygame.K_SPACE]:
                            self.vel_y = -20
                        if len(sticks) >= 1 and joyJump == True:
                            self.vel_y = -20

        #player y change                
        self.rect.y += y_change + scroll       

        #scroll check
        if self.rect.top <= SCROLL_TRESH:
            if self.vel_y < 0:
                scroll = -y_change
        
        return scroll    

        
#floor class            
class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(floorImg, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):
        #moving floor's y position
        self.rect.y += scroll

        #check if floor has gone
        if self.rect.y > 800:
            self.kill()
    

#ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        screen.blit(self.image, self.rect)


    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.y > 800:
            self.kill()

#output text functions
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

#score display
def draw_score():
    draw_text("Score: " + str(score), fontSmall, (255,255,255), 0, 0)

player = Player(300,725)
ground = Ground(0,750)

#sprite groups
floor_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

#starting floor
floor = Floor(250,590, 70)
floor_group.add(floor)


#game loop
run = True
while run:
    clock.tick(FPS)
    screen.fill((0,0,0))
    ground.draw()
    
    if gameOver == False:
        #generate floors
        if len(floor_group) < MAX_FLOOR:
            f_w = random.randint(60,120)
            f_x = random.randint(0, 600 - f_w)
            f_y = floor.rect.y - random.randint(80,120)
            floor = Floor(f_x, f_y, f_w)
            floor_group.add(floor) 
        
        #update scroll
        if scroll > 0:
            score += scroll

        #draw sprites
        floor_group.update(scroll)
        floor_group.draw(screen)
        player.drawPlayer()
        scroll = player.move()
        ground.update(scroll)

        #draw score
        draw_score()

        #check if game over
        if player.rect.top >= 800:
            gameOver = True
    else:
        floor_group.draw(screen)
        #blur
        s = pygame.Surface((600,800))
        s.set_alpha(50)        
        s.fill((255,255,255))    
        screen.blit(s, (0,0))
        draw_text('GAME OVER!', fontBig, (255,255,255), 242, 250)
        draw_text('Score: '+ str(score), fontBig, (255,255,255), 242, 300)
        if len(sticks) >= 1:
            draw_text('Press [ENTER] or [START] to play again.', fontSmall, (255,255,255), 160, 350)
        else:
            draw_text('Press [ENTER] to play again.', fontSmall, (255,255,255), 200, 350)
        key = pygame.key.get_pressed()
        #****this part could be written better 
        if key[pygame.K_RETURN]:
            gameOver = False
            score = 0
            scroll = 0
            #reposition
            player.rect.center = (300,725)
            floor_group.empty()
            #starting floor
            floor = Floor(250,590, 70)
            floor_group.add(floor)
            #reset ground
            ground.rect.x = 0
            ground.rect.y = 750
            ground_group.add(ground)
        if len(sticks) >= 1:
            if pygame.joystick.Joystick(0).get_button(7):
                gameOver = False
                score = 0
                scroll = 0
                #reposition
                player.rect.center = (300,725)
                floor_group.empty()
                #starting floor
                floor = Floor(250,590, 70)
                floor_group.add(floor)
                #reset ground
                ground.rect.x = 0
                ground.rect.y = 750
                ground_group.add(ground)

   

        

    pygame.display.update()
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()