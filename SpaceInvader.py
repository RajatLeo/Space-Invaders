import pygame
import math
import random
from pygame import mixer

pygame.init()

# window Setup
winsize = (800, 600)
background = pygame.image.load("background.png")
window = pygame.display.set_mode(winsize)
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# background Music
backmusic = mixer.music.load("Background.wav")
mixer.music.play(-1)

# player setup
playerImg = pygame.image.load("player.png")
playerX = 368
playerY = 520
playerSpeed = 0

# enemy setup
enemyImg = []
enemyX = []
enemyY = []
enemyXSpeed = []
enemyYSpeed = []
number_of_enemy = 2

# multiple-enemy setup
for i in range(number_of_enemy):
    if i < number_of_enemy // 2:
        enemyImg.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(25, 125))
        enemyXSpeed.append(random.randint(5, 10))
        enemyYSpeed.append(48)
    else:
        enemyImg.append(pygame.image.load("enemy2.png"))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(25, 125))
        enemyXSpeed.append(random.randint(10, 12))
        enemyYSpeed.append(24)

# bullet setup
bulletImg = pygame.image.load("bullet.png")
bulletX = 368
bulletY = 520
bulletXSpeed = 0
bulletYSpeed = 20
bulletState = "loaded"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

# victory and death music
played = False
victoryPlayed = False

# gameover
gameoverstatus = False

# level
level = 1
tempScore = 0
font = pygame.font.Font('freesansbold.ttf', 32)
levelX = 650
levelY = 10


def resetLevel():
    global level
    level = 1
    global enemyImg, enemyX, enemyY, enemyXSpeed, enemyYSpeed, number_of_enemy
    number_of_enemy = 2
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyXSpeed.clear()
    enemyYSpeed.clear()
    for i in range(number_of_enemy):
        if i < number_of_enemy // 2:
            enemyImg.append(pygame.image.load("enemy.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(25, 125))
            enemyXSpeed.append(random.randint(5, 10))
            enemyYSpeed.append(48)
        else:
            enemyImg.append(pygame.image.load("enemy2.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(25, 125))
            enemyXSpeed.append(random.randint(10, 12))
            enemyYSpeed.append(24)
    global tempScore, score
    score = 0
    tempScore = score


def increaseLevel():
    global level
    level += 1
    global enemyImg, enemyX, enemyY, enemyXSpeed, enemyYSpeed, number_of_enemy
    number_of_enemy += 2
    for i in range(2):
        if i % 2 == 0:
            enemyImg.append(pygame.image.load("enemy.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(25, 125))
            enemyXSpeed.append(random.randint(5, 10))
            enemyYSpeed.append(48)
        else:
            enemyImg.append(pygame.image.load("enemy2.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(25, 125))
            enemyXSpeed.append(random.randint(10, 12))
            enemyYSpeed.append(24)
    global tempScore, score
    tempScore = score


def displayLevel(x, y):
    levelImg = font.render("Level: " + str(level), True, (255, 255, 255))
    window.blit(levelImg, (x, y))


def displayScore(x, y):
    scoreImg = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(scoreImg, (x, y))


def collide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 30:
        return True
    else:
        return False


def firebullet(x, y):
    global bulletState
    bulletState = "fire"
    window.blit(bulletImg, (x + 16, y + 5))


def player(x, y):
    window.blit(playerImg, (x, y))


def enemy(x, y, i):
    window.blit(enemyImg[i], (x, y))


run = True
while run:
    window.fill((50, 50, 200))
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerSpeed = -10
            if event.key == pygame.K_RIGHT:
                playerSpeed = 10
            if event.key == pygame.K_SPACE and bulletState == "loaded":
                bulletsound = mixer.Sound('bullet.wav')
                bulletsound.play()
                bulletX = playerX
                firebullet(bulletX, bulletY)
            if event.key == pygame.K_RETURN and gameoverstatus == True:
                window.fill((50, 50, 200))
                window.blit(background, (0, 0))
                resetLevel()
                mixer.music.play(-1)
                playerY = 520
                bulletYSpeed = 15
                bulletX, bulletY = 368, 520
                gameoverstatus = False
                played = False
                victoryPlayed = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerSpeed = 0

    playerX += playerSpeed
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(number_of_enemy):
        enemyX[i] += enemyXSpeed[i]
        if enemyX[i] <= 0:
            enemyXSpeed[i] = abs(enemyXSpeed[i])
            enemyY[i] += enemyYSpeed[i]
        elif enemyX[i] >= 736:
            enemyXSpeed[i] = -abs(enemyXSpeed[i])
            enemyY[i] += enemyYSpeed[i]

        # Game Over
        if enemyY[i] >= 456:
            gameoverstatus = True
            for x in range(number_of_enemy):
                enemyY[x] = 2000
                pygame.mixer.music.stop()
                death = pygame.image.load("death.png")
                window.blit(death, (380, 250))
                gameover = pygame.image.load("gameover.png")
                window.blit(gameover, (350, 120))
                enterImg = font.render("Press Enter to Restart", True, (255, 0, 255))
                window.blit(enterImg, (250, 330))
                if played == False:
                    gameovermusic = mixer.Sound("gameover.wav")
                    gameovermusic.play()
                    played = True
            playerY = 2000
            bulletYSpeed = 0
            bulletX, bulletY = 2000, 2000

        # collision
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            if i < number_of_enemy // 2:
                die = mixer.Sound('die.wav')
                die.play()
            else:
                die = mixer.Sound('die1.wav')
                die.play()
            bulletY = 520
            bulletState = "loaded"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(25, 125)

        enemy(enemyX[i], enemyY[i], i)

    # win
    if score == 20:
        for x in range(number_of_enemy):
            enemyY[x] = -2000
            pygame.mixer.music.stop()
        youWin = pygame.image.load("win.png")
        window.blit(youWin, (350, 120))
        winImg = font.render("Congratulation Sergent, You Win", True, (255, 0, 255))
        window.blit(winImg, (165, 280))
        if victoryPlayed == False:
            won = mixer.Sound("won.wav")
            won.play()
            victoryPlayed = True
        gameoverstatus = True

    # level Increase
    if score == tempScore + 5:
        levelup = mixer.Sound("levelup.wav")
        levelup.play()
        increaseLevel()

    # bullet firing
    if bulletY <= 0:
        bulletY = 520
        bulletState = "loaded"

    if bulletState == "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletYSpeed

    player(playerX, playerY)
    displayScore(scoreX, scoreY)
    displayLevel(levelX, levelY)
    pygame.display.update()
