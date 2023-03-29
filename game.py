#----------------------------------------------------------------------------
# This template is written by Sean Deitrich and intended for use his students
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
import sys
import random
import math
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, NAME
from utility import *
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------

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
# Create Score Variables Here
#----------------------------------------------------------------------------
score = 0

#----------------------------------------------------------------------------
# Create Text Boxes Here
#----------------------------------------------------------------------------
#This creates a text box, but you'll have to add it to the level you want
titleText = Text(screen, "PyGame Template by: " + NAME, BLACK, 30,100,100)

#----------------------------------------------------------------------------
# Create Backgrounds Here
#----------------------------------------------------------------------------
titleScreenBackground = "background.jpg"
level1Background = "landscape.jpg"
#----------------------------------------------------------------------------
# Create Objects, Characters, Enemies, etc. Here
#----------------------------------------------------------------------------
player = Character("Hero.png", (100,100), (100,100)) #Image, (Width, Height), (X,Y)
player.set_speed(5) #Set the speed of the character when we control it

monster = Character("Monster.png", (100,100), (300,300))
monster.set_speed(5)
#TODO Enemy Example
#TODO Item Example

#----------------------------------------------------------------------------
# Create Levels Here
#----------------------------------------------------------------------------
#Step 1. Create the Level itself
titleScreen = Level(screen, titleScreenBackground)
titleScreen.addText(titleText) #Add text to it if you want

#Here's another example
level1 = Level(screen, level1Background)
#Then add Characters, Enemies, etc. to the level! The order matters.
#What you add first will be the furthest 'back'.
#What you add last will be the closes to the 'front'.
level1.add(monster)
level1.add(player)


#----------------------------------------------------------------------------
# Create Additional Timers Here if Needed
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
# Create Controls and Logic for Each Level Here
#----------------------------------------------------------------------------
def titleControls():
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                game.setLevel(level1) #Change the game to level1
                timer.start() #Start the timer

def level1Controls(keys_pressed):
    direction = pygame.math.Vector2() #Allows the player to have a direction
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            #----------------------------------------------------------------------------
            # Check to see if keys were JUST pressed here (not held)
            #----------------------------------------------------------------------------
            if event.key == pygame.K_SPACE: #If it was the space key
                newProjectile = MouseProjectile("laser.png", player.center, 10) #image, position, speed
                player.addProjectile(newProjectile) #Add the projectile to the player 

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
    player.move(direction)
    
    #Check for collision between the player and the monster
    if player.collidesWith(monster):
        print("Collision Detected")
    
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
        titleControls()
    elif game.currentLevel == level1:
        level1Controls(keys_pressed)

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
    pygame.display.update() #Update the display every frame
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# ▼▼▼ DO NOT WRITE CODE BELOW THIS LINE ▼▼▼ 
#----------------------------------------------------------------------------