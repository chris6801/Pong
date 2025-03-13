# Pygame test

import pygame, sys, random, math
from pygame.locals import *
pygame.init()
pygame.font.init()

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WIN_WIDTH = 680
WIN_HEIGHT = 480
CENTER = (WIN_WIDTH//2, WIN_HEIGHT//2)
CENTER_X = WIN_WIDTH//2
CENTER_Y = WIN_HEIGHT//2

# Colors
BCKGRND = (255, 255, 255)
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
CHAR_COL = (255, 30, 70)

# Classes
class Paddle:
    def __init__(self, color, AI=False):
        self.x = 30
        self.y = CENTER_Y
        self.dx = 0
        self.dy = 0
        self.w = 15
        self.h = 45
        self.color = color
        self.AI = AI
        
    def update(self, ball):
        #AI if computer controlled
        if self.AI is True:
            if ball.y > self.y + (self.h / 2):
                self.dy = 5 * (1 - (self.x - ball.x))
            if ball.y < self.y + (self.h / 2):
                self.dy = -5 * (1 - (self.x - ball.x))
        
        self.x += self.dx
        self.y += self.dy
        
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self)

class Ball:
    def __init__(self, radius, color):
        self.x = CENTER_X
        self.y = CENTER_Y
        self.dx = 0
        self.dy = 0
        self.r = radius
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x, self.y), self.r)
        
# Objects

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Test")

# Functions



# Main Function
def main():
    looping = True

    ScoreFont = pygame.font.SysFont(None, 24)
    Score1 = 0
    Score2 = 0

    Paddle1X = 30
    Paddle1Y = 240
    Paddle1Width = 15
    Paddle1Height = 45
    Paddle1V = 0

    Paddle2X = WIN_WIDTH - 30
    Paddle2Y = WIN_HEIGHT/2
    Paddle2Width = 15
    Paddle2Height = 45
    Paddle2V = 0
    
    BallX = WIN_WIDTH/2
    BallY = WIN_HEIGHT/2
    BallRad = 5
    BallSurface = WINDOW
    BallColor = BLUE
    pi = math.pi
    BallAngle = 5*pi/6
    VMag = 2


    

    # Main Loop
    while looping:

        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == K_r:
                Paddle1 = 30 
                Paddle1Y = WIN_HEIGHT/2

        pressed = pygame.key.get_pressed()
        if (pressed[K_DOWN]):
            Paddle1V = 5
            Paddle1Y = Paddle1Y + Paddle1V
            Paddle1V = Paddle1V + 1
            if Paddle1V >= 8:
                Paddle1V = 8
    
        if (pressed[K_UP]):
            Paddle1V = - 5
            Paddle1Y = Paddle1Y + Paddle1V
            Paddle1V = Paddle1V - 1
            if Paddle1V <= -8:
                Paddle1V = -8
    
        if not (pressed[K_UP]) and not (pressed[K_DOWN]):
            Paddle1V = 0
        


        # Processing
        Paddle1 = Rect(Paddle1X, Paddle1Y, Paddle1Width, Paddle1Height)
        Paddle2 = Rect(Paddle2X, Paddle2Y, Paddle2Width, Paddle2Height)
        BallXVelocity = math.cos(BallAngle) * VMag
        BallYVelocity = math.sin(BallAngle) * VMag
        Score1Display = ScoreFont.render(str(Score1), True, RED)
        Score2Display = ScoreFont.render(str(Score2), True, RED)

        #AI
        if BallY > Paddle2Y + (Paddle2Height/2):
            Paddle2V = 5 * (1-(Paddle2X-BallX))
            Paddle2Y = Paddle2Y + Paddle2V
        if BallY < Paddle2Y + (Paddle2Height/2):
            Paddle2V = -5 * (1-(Paddle2X-BallX))
            Paddle2Y = Paddle2Y + Paddle2V
        

        ## Simple conditions Reflections for the ceiling boundaries
        if Paddle1Y < 0:
            Paddle1Y = 0
        if Paddle1Y > WIN_HEIGHT - Paddle1Height:
            Paddle1Y = WIN_HEIGHT - Paddle1Height
        if Paddle2Y < 0:
            Paddle2Y = 0
        if Paddle2Y > WIN_HEIGHT - Paddle2Height:
            Paddle2Y = WIN_HEIGHT - Paddle2Height
    
        if BallY < 0:
            BallY = 5
            BallAngle = 2*pi - BallAngle
        if BallY > WIN_HEIGHT:
            BallY = WIN_HEIGHT - 5
            BallAngle = 2*pi - BallAngle
        

        ## Scoring Condition
        if BallX > WIN_WIDTH:
            BallX = CENTER_X
            BallY = CENTER_Y
            BallAngle = - pi - BallAngle
            Score1 = Score1 + 1
        if BallX < 0:
            BallX = CENTER_X
            BallY = CENTER_Y
            BallAngle = - pi - BallAngle
            Score2 = Score2 + 1

        ## Collision Detection with Paddle. If the paddle isn't moving we use the simple reflection if
        ## it's moving we set the angle to the opposite direction plus an angle proportional to the
        ## paddle velocity
        if BallX < Paddle1X + Paddle1Width + 1 and BallX > Paddle1X + Paddle1Width - 1 \
            and (BallY < Paddle1Y + Paddle1Height and BallY > Paddle1Y):
            BallX = BallX + 3
            if Paddle1V == 0:
                BallAngle = - pi - BallAngle 
            else:
                BallAngle = 0
                BallAngle = BallAngle - (Paddle1V*.3925*pi)
        if BallX > Paddle2X - 1 and BallX > Paddle2X + 1 and \
            (BallY < Paddle2Y + Paddle2Height and BallY > Paddle2Y):
            BallX = BallX - 3
            if Paddle2V == 0:
                BallAngle = - pi - BallAngle
            else:
                BallAngle = pi
                BallAngle = BallAngle - (Paddle2V*.3925*pi)
        
        BallX = BallX + BallXVelocity
        BallY = BallY - BallYVelocity

        # Render elements of the game 
        WINDOW.fill(BCKGRND)
        pygame.draw.rect(WINDOW, BLUE, Paddle1)
        pygame.draw.rect(WINDOW, GREEN, Paddle2)
        pygame.draw.circle(BallSurface, BallColor, (BallX, BallY), BallRad)
        WINDOW.blit(Score1Display, (40, 40)) 
        WINDOW.blit(Score2Display, (WIN_WIDTH - 40, 40))
        pygame.display.update()
        fpsClock.tick(FPS)

main()