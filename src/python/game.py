#!/usr/bin/python

import sys
import pygame
import time

# Game variables
width = 640
height = 480
color_blue = (0, 0, 64)

pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # load image
        self.image = pygame.image.load('../resources/ball_20x20.png')

        # get rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.centery = height / 2
        self.speed = [3 , 3]

    def update(self):

        # Control out of display
        if self.rect.top <= 0:
            self.speed[1] = -1 * self.speed[1]

        elif self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -1 * self.speed[0]

        # Move ball taking position and speed into account
        self.rect.move_ip(self.speed)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # load image
        self.image = pygame.image.load('../resources/player.png')

        # get rectangle
        self.rect = self.image.get_rect()
        self.rect.midbottom = (width / 2 , height - 20)
        self.speed = [0 , 0]

    def update(self, event):
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-8 , 0]

        elif event.key == pygame.K_RIGHT and self.rect.right < width:
            self.speed = [8, 0]

        else:
            self.speed = [0,0]

        self.rect.move_ip(self.speed)


class Brick(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        # load image
        self.image = pygame.image.load('../resources/brick.png')

        # get rectangle
        self.rect = self.image.get_rect()

        self.rect.topleft = location


class Wall(pygame.sprite.Group):
    def __init__(self, size):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20

        for i in range(size):
            brick = Brick((pos_x, pos_y))
            self.add(brick)
            pos_x += brick.rect.width

            if pos_x > width:
                pos_x = 0
                pos_y += brick.rect.height



def gameOver():
    font = pygame.font.SysFont('Arial', 72)
    text = font.render('Game Over :/', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = [width / 2 , height / 2]
    display.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit(0)

def showScore():
    font = pygame.font.SysFont('Consolas', 20)
    text = font.render('Score {0}'.format(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = [0, 0]
    display.blit(text, text_rect)

# Initialize window
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('BreakOut Game')

# Initialize pygame Clock
fps = pygame.time.Clock()

# Keyboard repetitions
pygame.key.set_repeat(30)

# Create playables
myBall = Ball()
myPlayer = Player()
myWall = Wall(50)
score = 0

# Game loop
while True:

    fps.tick(60)

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:
            myPlayer.update(event)

    # Update elements in screen
    myBall.update()


    # Collition detector
    if pygame.sprite.collide_rect(myBall, myPlayer):
        myBall.speed[1] = -1 * myBall.speed[1]

    myList = pygame.sprite.spritecollide(myBall, myWall, False)
    if myList:
        brick = myList[0]
        cx = myBall.rect.centerx

        # x axis collition
        if cx < brick.rect.left or cx > brick.rect.right:
            myBall.speed[0] *= -1
        else:
            myBall.speed[1] *= -1

        myWall.remove(brick)
        score += 10

    if myBall.rect.bottom > height:
        gameOver()

    display.fill(color_blue)
    showScore()

    # Draw screen
    display.blit(myBall.image, myBall.rect)
    display.blit(myPlayer.image, myPlayer.rect)
    myWall.draw(display)

    pygame.display.flip()