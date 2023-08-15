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
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, NAME, FPS
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
# Title Screen
#----------------------------------------------------------------------------
titleScreenBackground = "background.jpg"
titleScreen = Level(screen, titleScreenBackground)
titleText = Text(screen, "PyGame Template by: " + NAME, BLACK, 30,100,100)
titleScreen.addText(titleText) 

#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
game = Game(titleScreen) #Create a game with the starting level as titleScreen
gameRunning = True #Ensure the game is running

def checkQuit(event):
    global gameRunning
    if event.type == pygame.QUIT: #If the close (X) button is pressed
        gameRunning = False #The game ends
        pygame.quit() #PyGame Quits
        sys.exit() #The window exits
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲ 
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Level 1
#----------------------------------------------------------------------------
level1Background = "landscape.jpg" #Background for level 1

score = 0 #This is a variable called 'score' that starts at 0 in level 1. We can change it to keep track of the score.
playerpickedup = False #This variable keeps track of whether or not the player is picked up with the mouse

player = Character("Hero.png", (100,100), (100,100)) #Image, (Width, Height), (X,Y)
player.setSpeed(5) #Set the speed of the character when we control it
walking = Animation("walking.png", 1, 24) #Filename, Rows, Cols (You can add another number (1-60) to control the speed of the animation)
player.addAnimation(walking)
player.animated = True #This allows the player to use their animation

laserSound = Sound("laser.wav") #This creates a sound, but doesn't play it - you'll see that later in the code

monster = Character("Monster.png", (100,100), (300,300)) #This creates a monster character with a size of (100,100) and position (300,300)
monster.setSpeed(5) #Sets the speed of the monster when it moves

#Creates the actual level
level1 = Level(screen, level1Background)

#Adds the monster and the player to level 1
level1.add(monster)
level1.add(player)

#Creates a usable timer that can start, stop, and reset
timer = Timer()
#----------------------------------------------------------------------------
# LEVEL CONTROLS: Create Controls and Logic for Each Level Here
#----------------------------------------------------------------------------
def titleLogic():
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                game.setLevel(level1) #Change the game to level1
                timer.start() #Start the timer

def level1Logic(keys_pressed):
    global score, playerpickedup #Tells this level to use the score and playerpickedup variables at the top of the code
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        #----------------------------------------------------------------------------
        # KEYS: Check to see if keys were JUST pressed here (not held)
        #----------------------------------------------------------------------------
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                newProjectile = MouseProjectile("laser.png", player.top, 10) #image, position, speed
                player.addProjectile(newProjectile) #Add the projectile to the player 
                laserSound.play() #Play the laser sound
        #----------------------------------------------------------------------------
        # MOUSE: Check to see if things were clicked on here!
        #----------------------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.clicked():
                playerpickedup = True
        #----------------------------------------------------------------------------
        # MOUSE: Check to see if the mouse button was released here!
        #----------------------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            playerpickedup = False
    #----------------------------------------------------------------------------
    # KEYS: Check to see if keys are HELD here!
    #----------------------------------------------------------------------------  
    #This method is used to check to see when keys are HELD
    direction = pygame.math.Vector2() #Allows the player to have a direction
    if keys_pressed[pygame.K_d]:
        direction.x = 1
        player.flipHorizontal(False)
    if keys_pressed[pygame.K_a]:
        direction.x = -1
        player.flipHorizontal(True)
    if keys_pressed[pygame.K_w]:
        direction.y = -1
    if keys_pressed[pygame.K_s]:
        direction.y = 1

    #Enable movement for the player based on the direction
    player.move(direction)
    
    #If the player is picked up, match it's position to the mouse position
    if playerpickedup:
        player.setPosition(pygame.Vector2(pygame.mouse.get_pos()))
    #Check for collision between the player and the monster
    if player.collidesWith(monster):
        print("Player is Colliding with Monster!")
    #Check for collision between any of the player's projectiles and the monster
    if player.projectilesCollideWith(monster):
        print("Projectile Collided with Monster!")
    
    #level1.background.scroll(-1,0) #Scrolling background
#----------------------------------------------------------------------------
# ▼▼▼ DO NOT ADJUST THIS CODE ▼▼▼ 
#----------------------------------------------------------------------------
while gameRunning: #While the game is running
    screen.fill(RED) #Fill the screen with red
    clock.tick(FPS) #Runs the game at 60FPS
    keys_pressed = pygame.key.get_pressed()
    game.run() #Display the current level in the game
#----------------------------------------------------------------------------
# ▲▲▲ DO NOT ADJUST THIS CODE ▲▲▲
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# Input Processing for Each Level Goes Here 
#----------------------------------------------------------------------------
    if game.currentLevel == titleScreen:
        titleLogic()
    elif game.currentLevel == level1:
        level1Logic(keys_pressed)

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