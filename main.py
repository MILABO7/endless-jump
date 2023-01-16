import pygame

# pygame initialization
pygame.init()

win = pygame.display.set_mode((600,800))
clock = pygame.time.Clock()

#character
character = pygame.image.load('player.png')
char = character.get_rect()
char.x = 300
char.y = 700
charX_change = 0

#ground
groundImg = pygame.image.load('ground.png')

#floors
floorImg = pygame.image.load('floor.png')
floorRect = floorImg.get_rect()
floorRect.x = 200
floorRect.y = 500

gravity = 1

def player(x,y):
    win.blit(character, (x,y))

def ground():
    win.blit(groundImg, (0,750))

def floor():
    win.blit(floorImg, (floorRect.x, floorRect.y))


isJump = False
jumpVel = 10

print(char)

running = True
while running:
    win.fill((0,0,0))
    ground()
    floor()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        char.x += -10
    if keys[pygame.K_RIGHT]:
        char.x += 10
    
    #jumping
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    if isJump:
        char.y -= jumpVel * 7
        jumpVel -= 1
        if jumpVel < -10:
            isJump = False
            jumpVel = 10

    #bounderies
    if char.x <= 0:
        char.x = 560
    elif char.x >= 580:
        char.x = 0

    if char.colliderect(floorRect):
        char.y = floorRect.y
        
        
    

    
    
      

    player(char.x, char.y)
    pygame.time.delay(20)
    clock.tick(60)
    pygame.display.update()
    