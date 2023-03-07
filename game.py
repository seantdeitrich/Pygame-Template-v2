import pygame, sys, random, time, math
from utility import *
#----------------------------------------------------------------------------
# Create/Adjust Constants Here
#----------------------------------------------------------------------------
WIDTH = 500
HEIGHT = 500
NAME = "Sean Deitrich"
GAME_NAME = "Sean's Game"
#----------------------------------------------------------------------------
# Create Colors Here
#----------------------------------------------------------------------------
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
# Create Backgrounds Here
#----------------------------------------------------------------------------
level1background = "background.jpg"
level2background = "landscape.jpg"
#----------------------------------------------------------------------------
# Create Objects, Characters, Enemies, etc. Here
#----------------------------------------------------------------------------
r = Block(RED, 100, 100, 100, 100)#Color, Width, Height, X Location, Y Location
g = Block(GREEN, 100, 100, 150, 100)
b = Block(BLUE, 100, 100, 200, 100)

#----------------------------------------------------------------------------
# Create Levels Here
#----------------------------------------------------------------------------
#Step 1. Create an ordered list of characters, objects, and things that will be in the level
#Note: The order of this matters! Pay attention to what you want the furthest back in your game, and put the first in the list
#Whatever you want in front, should be last in the list.
titleSprites = [r,g,b] 
#Step 2. Create the Level itself
titleScreen = Level(screen, level1background, titleSprites)

level1Sprites = []
level1 = Level(screen, level2background, level1Sprites)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
game = Game(titleScreen) #Create a game with the starting level as titleScreen
gameRunning = True #Ensure the game is running
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲ 
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Create Controls for Each Level Here
#----------------------------------------------------------------------------
def titleControls(event):
    if event.type == pygame.KEYDOWN: #When any key is pressed down
        if event.key == pygame.K_SPACE: #If it was the space key
            game.currentLevel = level1 #Change the game to level1

def level1Controls(event):
    if event.type == pygame.KEYDOWN: #When any key is pressed down
        if event.key == pygame.K_SPACE: #If it was the space key
            print("Hit Space in Level 1") #Print that we hit space in level 1


#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
while gameRunning: #While the game is running
    screen.fill(RED) #Fill the screen with red
    clock.tick(60) #Runs the game at 60FPS
    for event in pygame.event.get(): #Check to see whats happening in the game
        if event.type == pygame.QUIT: #If the close (X) button is pressed
            gameRunning = False #The game ends
            pygame.quit() #PyGame Quits
            sys.exit() #The window exits
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Input Processing for Each Level Goes Here 
#----------------------------------------------------------------------------
        elif game.currentLevel == titleScreen:
            titleControls(event)
        elif game.currentLevel == level1:
            level1Controls(event)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
        game.display() #Display the current level in the game
        pygame.display.update() #Update the display every frame

