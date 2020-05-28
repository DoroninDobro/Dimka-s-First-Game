import pygame
import math
import random
from copy import copy
from pygame import mixer

# intialize the pygame
pygame.init()

OVERbool = 0
OVERimg = pygame.font.Font('UF.otf', 128)
OVER = OVERimg.render('GAME OVER', 1, (255,0,0))

# add screen
screen = pygame.display.set_mode((800, 600))

# made a fon
fon = pygame.image.load('fon.jpg')

# fon sound
mixer.music.load('EM.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("UNDERLIVE")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerXspeed = 0
playerYspeed = 0

# enemy
enemynum = 1
enemyimg = pygame.image.load('galaxy.png')
enemyX = []
enemyY = []
enemyXspeed = []
enemyYspeed = []
enemyHP = []
for i in range(120):
    enemyHP.append(2)
    enemyX.append(random.randint(50, 750))
    enemyY.append(50)
    enemyXspeed.append(random.randint(3, 6))
    enemyYspeed.append(random.choice([0.3, 0.4, 0.5, 0.6]))
# bullet
# ready - you can't see bullet now
# fire - bullet move now
bulletimg = pygame.image.load('bullet.png')
bulletY = 480
bulletX = 0
bulletXspeed = 0
bulletYspeed = 10
bulletstate = 'ready'
# Score
scoreN = 0
scoreimg = pygame.font.Font('UF.otf', 32)
scoreX = 10
scoreY = 10

# TimeBonus
TimeBonusN = 0
TimeBonusimg = pygame.font.Font('UF.otf', 32)
TimeBonusX = 550
TimeBonusY = 10

def score(x, y):
    score = scoreimg.render('SCORE: ' + str(scoreN), 1, (50,50,255))
    screen.blit(score, (x, y))

def TimeBonus(x, y):
    TimeBonus = TimeBonusimg.render('TimeBonus: ' + str(TimeBonusN), 1, (255,255,0))
    screen.blit(TimeBonus, (x, y))

def player(X, Y):
    screen.blit(playerimg, (X, Y))

def enemy(X, Y):
    screen.blit(enemyimg, (X, Y))

def bulletfire(x, y):
    global bulletstate
    bulletstate = 'fire'
    screen.blit(bulletimg, (x + 20, y + 10))

def boom(X1, Y1, X2, Y2):
    dist = math.sqrt((math.pow(X1 - X2, 2)) + (math.pow(Y1 - Y2, 2)))
    if dist < 27:
        return 1
    else:
        return 0

# game loop
run = 1
while run:
    
    # RGB
    screen.fill((0, 0, 50))
    
    # fon image
    screen.blit(fon, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXspeed = -5
            if event.key == pygame.K_RIGHT:
                playerXspeed = 5
            if event.key == pygame.K_SPACE :
                if bulletstate is "ready":
                    # Get the current x cordinate of the spaceship
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    bulletfire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXspeed = 0

    # for hero not vanish
    if playerX > 736:
        playerX = 736
    if playerX < -1.0:
        playerX = -1.0

    # for enemy not vanish
    for i in range(enemynum):
        if enemyX[i] > 736:
            enemyXspeed[i] = 0-(enemyXspeed[i])
        if enemyX[i] < 0:
            enemyXspeed[i] = 0-(enemyXspeed[i])

    # bullet move
    if bulletY<=0:
        bulletY = playerY
        bulletX = playerX
        bulletstate = 'ready'
    if bulletstate == 'fire':
        bulletfire(bulletX, bulletY)
        bulletY -= bulletYspeed
    
    # collision
    for i in range(enemynum):
        collision = boom(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            boomSound = mixer.Sound('BOOM.wav')
            boomSound.play()
            enemyHP[i] -= 1
            bulletY = 480
            bulletX = playerX
            bulletstate = 'ready'

    # Enemy dead
    for i in range(enemynum):
        print(i)
        if enemyHP[i] == 0:
            scoreN += 1000
            enemyX[i] = random.randint(50, 750)
            enemyY[i] = 50
            enemyHP[i] = 2
    
    # GAME OVER
    for i in range(enemynum):
        if enemyY[i] >= 500:
            screen.blit(OVER, (130, 250))
            OVERbool = 1
            for i in range(enemynum):
                enemyY[i] = 4654765866556656556
            
    for i in range(enemynum):
        enemyY[i] += enemyYspeed[i]
        enemyX[i] += enemyXspeed[i]
        enemy(enemyX[i], enemyY[i])
    playerX += playerXspeed
    playerY += playerYspeed
    player(playerX, playerY)
    if OVERbool == 0:
        TimeBonusN += 2
        enemynum = int(scoreN / 5000) + 1
    TimeBonus(TimeBonusX, TimeBonusY)
    score(scoreX, scoreY)
    pygame.display.update()
