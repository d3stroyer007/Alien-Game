#importing libraries rarandomndom
import pygame
import sys
import random
import math
from pygame import mixer
from PIL import Image

#Initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((1000, 700))


#setting title and icon
pygame.display.set_caption("Endless Runner Game")
pygame.display.set_icon(pygame.image.load("run.png"))
background = pygame.image.load("background.jpg")
background_music = mixer.music.load('background (1).wav')
mixer.music.play(-1)

#creating and controlling runner
runner = pygame.image.load("spaceship.png")
runner_X = 400
runner_Y = 550
runner_X_change = 0
runner_Y_change = 0
score = 0
game_over_font = pygame.font.Font('PINEON.ttf', 60)

#creating and controlling bullet
bullet = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 550
bullet_X_change = 0
bullet_Y_change = 25
#ready means the bullet is hidden
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('PINEON.ttf', 30)
text_x = 20
text_y = 625

def show_score(X, Y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (X, Y))

#fire means the bullet is shot and moving

#creating enemy
aliens = []
alien_X_change = []
alien_Y_change = []
alien_X = []
alien_Y = []
number_of_aliens = 6

for i in range(number_of_aliens):
    aliens.append(pygame.image.load("enemy_spaceship.png"))
    alien_X.append(random.randint(50, 950))
    alien_Y.append(random.randint(50, 200))
    alien_X_change.append(5)
    alien_Y_change.append(25)



def Runner(X, Y):
    screen.blit(runner, (X, Y))
def Aliens (X, Y,i):
    screen.blit(aliens[i], (X, Y))
def Fire_Bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (X + 16, Y))
def collision_detection(alien_X, alien_Y, bullet_X, bullet_Y):
    distance = math.sqrt((math.pow(alien_X - bullet_X, 2) + (math.pow(alien_Y - bullet_Y, 2))))
    if distance < 32:
        return True
    else:
        return False

def game_over_text():
    game_over_text = game_over_font.render("GAME \nOVER", True, (200, 0, 0))
    screen.blit(game_over_text, (320, 300))

game_over = False
run = True
while True:

    # R, G, B = Red, Green, Blue
    screen.fill((0, 0, 0))
    screen.blit(background,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #when any key is pressed
            if event.key == pygame.K_LEFT:
                runner_X_change = -5
            if event.key == pygame.K_RIGHT:
                runner_X_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser (1).wav")
                    bullet_sound.play()
                    bullet_X = runner_X
                    Fire_Bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                runner_X_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                runner_Y_change = 0


    runner_X += runner_X_change
    if runner_X <= 0:
        runner_X = 0.5
    elif runner_X >= 936:
        runner_X = 936

    for i in range(number_of_aliens):

        #game over logic
        if alien_Y[i] > 450:
            for j in range(number_of_aliens):
                alien_Y[j] = 2000
            game_over_text()
            break

        alien_X[i] += alien_X_change[i]
        if alien_X[i] <= 0:
           alien_X_change[i] = 2.5
           alien_Y[i] += alien_Y_change[i]
        elif alien_X[i] >= 936:
           alien_X_change[i] = -2.5
           alien_Y[i] += alien_Y_change[i]
        is_collision = collision_detection(alien_X[i], alien_Y[i], bullet_X, bullet_Y)
        if is_collision:
            explosion_sound = mixer.Sound("explosion (1).wav")
            explosion_sound.play()
            bullet_Y = 600
            bullet_state = "ready"
            score_value += 1
            # Aliens(alien_X, alien_Y)
           # print(f"You're score is {score}"  )
            alien_X[i]=random.randint(50,950)
            alien_Y[i]=random.randint(50,250)
        Aliens(alien_X[i], alien_Y[i],i)


    runner_Y += runner_Y_change
    #updating display

    #bullet movement
    if bullet_Y <= 0:
        bullet_Y = 550
        bullet_state = 'ready'
    if bullet_state == 'fire':
        Fire_Bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_change


    #game_over_text()
    Runner(runner_X, runner_Y)
    show_score(text_x, text_y)
    pygame.display.update()