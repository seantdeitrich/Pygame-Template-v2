import sys
import random
import math
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, NAME
from utility import *
#----------------------------------------------------------------------------
# Create Colors Here
#----------------------------------------------------------------------------
#The three numbers in the parens are the red, green, and blue values
#They are always on a scale of 0 to 255. Google "Color Picker"!

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
pygame.init()
pygame.key.set_repeat() #Controls how held keys are repeated (delay, interval) -- See PyGame docs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Create Text Boxes Here
#----------------------------------------------------------------------------
#This creates a text box, but you'll have to display it in the level you want

titleText = Text(screen, "Title Screen", BLACK, 30,100,100)

#----------------------------------------------------------------------------
# Create Backgrounds Here
#----------------------------------------------------------------------------
titleScreenBackground = "background.jpg"
level1Background = "landscape.jpg"
#----------------------------------------------------------------------------
# Create Objects, Characters, Enemies, etc. Here
#----------------------------------------------------------------------------
redblock = Block(RED, 100, 100, 100, 100)#Color, Width, Height, X Location, Y Location
redblock.set_speed(10) #Set the speed of the red block when we control it

greenblock = Block(GREEN, 100, 100, 150, 100)
blueblock = Block(BLUE, 100, 100, 200, 100)

#----------------------------------------------------------------------------
# Create Levels Here
#----------------------------------------------------------------------------
#Step 1. Create an ordered list of characters, objects, and things that will be in the level
#Note: The order of this matters! Pay attention to what you want the furthest back in your game, and put the first in the list
#Whatever you want in front, should be last in the list.
titleSprites = [] 
#Step 2. Create the Level itself
titleScreen = Level(screen, titleScreenBackground, titleSprites)
#Here's another example
level1Sprites = [redblock, greenblock, blueblock]
level1 = Level(screen, level1Background, level1Sprites)

#----------------------------------------------------------------------------
# Create Timers Here
#----------------------------------------------------------------------------
timer = Timer()

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
game = Game(titleScreen) #Create a game with the starting level as titleScreen
gameRunning = True #Ensure the game is running

def checkQuit(event):
    if event.type == pygame.QUIT: #If the close (X) button is pressed
        gameRunning = False #The game ends
        pygame.quit() #PyGame Quits
        sys.exit() #The window exits
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲ 
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Create Controls for Each Level Here
#----------------------------------------------------------------------------
def titleControls(keys_pressed):
    titleText.display()
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                game.setLevel(level1) #Change the game to level1
                timer.start() #Start the timer

def level1Controls(keys_pressed):
    direction = pygame.math.Vector2() #Don't worry about what this is for now
    #This method is used to check if keys were JUST pressed
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                print("Hit Space in Level 1: " + str(timer.time())) #Print that we hit space in level 1 and the time on the timer
            if event.key == pygame.K_t:
                timer.restart()
        
    #This method is used to check to see when keys are HELD
    if keys_pressed[pygame.K_d]:
        direction.x = 1
    if keys_pressed[pygame.K_a]:
        direction.x = -1
    if keys_pressed[pygame.K_w]:
        direction.y = -1
    if keys_pressed[pygame.K_s]:
        direction.y = 1

    #Enable movement for the block (player)
    redblock.move(direction)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
while gameRunning: #While the game is running
    screen.fill(RED) #Fill the screen with red
    clock.tick(60) #Runs the game at 60FPS
    keys_pressed = pygame.key.get_pressed()
    game.run() #Display the current level in the game
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Input Processing for Each Level Goes Here 
#----------------------------------------------------------------------------
    if game.currentLevel == titleScreen:
        titleControls(keys_pressed)


    elif game.currentLevel == level1:
        level1Controls(keys_pressed)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
    pygame.display.update() #Update the display every frame

