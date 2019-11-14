#!/usr/bin/env python

import pygame
from random import randint

#init
pygame.init()
clock = pygame.time.Clock()

#set window
winWidth = 288
winheight = 510
win = pygame.display.set_mode((winWidth, winheight))
pygame.display.set_caption("Vaiby Birdy !!")
bgPaths = ['assets/sprites/background-day.png', 'assets/sprites/background-night.png']
bg = pygame.image.load(bgPaths[0])

## tiles space 
difficulty = 15

def renderStartWindow():
    win.blit(bg, (0,0))
    startwin = Startwin(130, 275, 12, 9)
    startwin.draw(win)
    pygame.display.update()

def renderPlayWindow():
    win.blit(bg, (0,0))
    bird.draw(win)
    pipes.draw(win, difficulty)
    pygame.display.update()

def renderGameOverWindow():
    win.blit(bg, (0,0))
    gameOver = Gameover(50, 155)
    gameOver.draw(win)
    pygame.display.update()

class Startwin:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0
        self.birdymid = pygame.image.load('assets/sprites/bluebird-midflap.png')
        self.logo = pygame.image.load('assets/sprites/logo_transparent.png')
        self.myfont = pygame.font.Font('assets/font/pacifico/Pacifico.ttf', 15)
        self.textsurface = self.myfont.render('Press Enter to continue', False, (0, 128, 0))

    def draw(self, win):
        self.win = win
        win.blit(self.logo, (5, 10))
        win.blit(self.birdymid, (self.x, self.y))
        win.blit(self.textsurface,(self.x - 50, self.y + 30))

class Bird:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gravity = 4
        self.jumpCount = 15
        self.isJumping = False
        self.jumpClicks = 0
        self.bird = [pygame.image.load('assets/sprites/bluebird-midflap.png'), pygame.image.load('assets/sprites/bluebird-upflap.png'), pygame.image.load('assets/sprites/bluebird-midflap.png'), pygame.image.load('assets/sprites/bluebird-downflap.png')]

    def draw(self, win):
        if self.jumpCount + 1 >= 32:
            self.jumpCount = 0
        if self.isJumping:
            win.blit(self.bird[1], (self.x, self.y))
        else:
            win.blit(self.bird[3], (self.x, self.y))

class Pipes:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pipe = pygame.image.load('assets/sprites/pipe-green.png')
        
    def draw(self, win, difficulty):
        win.blit(self.pipe, (self.x, winheight - self.y - difficulty))
        win.blit(pygame.transform.flip(self.pipe, False, True), (self.x, 0 - self.y + difficulty))

class Gameover:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bg = pygame.image.load("assets/sprites/gameover.png")

    def draw(self, win):
        win.blit(self.bg, (self.x, self.y))

if __name__ == "__main__":
    started = False
    bird = Bird(40, 240, 12, 8)
    pipVel = 0
    pipe = []   
    gameOver = False 
    #main loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if started == False:
                        started = True
                elif event.key == pygame.K_UP:
                    if not(gameOver):
                        bird.isJumping = True
                        bird.jumpClicks += 1

        keys = pygame.key.get_pressed()

        if started == False:
            renderStartWindow()
        else:
            if not(bird.isJumping):
                bird.jumpClicks = 0
                bird.y += bird.gravity
            else:
                if bird.jumpCount >= 0:
                    bird.y -= bird.jumpCount
                    bird.jumpCount -= 1
                else:
                    bird.isJumping = False
                    bird.jumpCount = 15

            if len(pipe) == 0: 
                pipX = winWidth
                pipY = randint(150,250)  
                pipes = Pipes(pipX, 200)
                pipe.append(pipes)
            else:
                if (bird.x > pipX and bird.x < pipX + 50) and (bird.y > winheight + difficulty - pipY or bird.y < 0 - pipY + difficulty + 330):
                    pipVel = 0
                    gameOver = True
                else:
                    pipVel = 3.0
                    pipX -= pipVel
                    if pipX <= -60:
                        pipe.pop(0)
                        pipVel = 0
                    else:
                        pipes = Pipes(pipX, pipY)
            if gameOver:
                renderGameOverWindow()
                gameOver = False
                started = False
            else:
                renderPlayWindow()
    pygame.quit()

