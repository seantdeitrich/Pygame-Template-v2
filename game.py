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
# Create Score, Health, Ammo, and Other Variables Here
#----------------------------------------------------------------------------
score = 0
playerpickedup = False

#----------------------------------------------------------------------------
# Create Text Boxes Here
#----------------------------------------------------------------------------
#This creates a text box, but you'll have to add it to the level you want
titleText = Text(screen, "PyGame Template by: " + NAME, BLACK, 30,100,100)

#----------------------------------------------------------------------------
# Create Spritesheets and Animations here
#----------------------------------------------------------------------------
walking = Animation("walking.png", 1, 24) #Filename, Rows, Cols (You can add another number (1-60) to control the speed of the animation)
#----------------------------------------------------------------------------
# Create Sounds and Music Here
#----------------------------------------------------------------------------
#Make sure the wav or mp3 file is in the sounds folder!
laserSound = Sound("laser.wav") #This creates a sound, but doesn't play it - you'll see that later in the code

#----------------------------------------------------------------------------
# Create Backgrounds Here
#----------------------------------------------------------------------------
titleScreenBackground = "background.jpg"
level1Background = "landscape.jpg"
#----------------------------------------------------------------------------
# Create Objects, Characters, Enemies, etc. Here
#----------------------------------------------------------------------------
player = Character("Hero.png", (100,100), (100,100)) #Image, (Width, Height), (X,Y)
player.setSpeed(5) #Set the speed of the character when we control it
player.addAnimation(walking)
#player.animated = True

monster = Character("Monster.png", (100,100), (300,300))
monster.setSpeed(5)

#----------------------------------------------------------------------------
# LEVELS: Create Levels Here
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
# TIMERS: Create Additional Timers Here if Needed
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
# LEVEL CONTROLS: Create Controls and Logic for Each Level Here
#----------------------------------------------------------------------------
def titleControls():
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                game.setLevel(level1) #Change the game to level1
                timer.start() #Start the timer

def level1Controls(keys_pressed):
    global playerpickedup #Tells this level to use the playerpickedup variable at the top of the code
    direction = pygame.math.Vector2() #Allows the player to have a direction
    for event in pygame.event.get(): #Check to see whats happening in the game
        checkQuit(event) #Check to see if the user quit the game, should be in every level
        #----------------------------------------------------------------------------
        # KEYS: Check to see if keys were JUST pressed here (not held)
        #----------------------------------------------------------------------------
        if event.type == pygame.KEYDOWN: #When any key is pressed down
            if event.key == pygame.K_SPACE: #If it was the space key
                newProjectile = MouseProjectile("laser.png", player.center, 10) #image, position, speed
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

    #If the player is picked up, match it's position to the mouse position
    if playerpickedup:
        player.position = pygame.Vector2(pygame.mouse.get_pos())

    #Enable movement for the player based on the direction
    player.move(direction)
    
    #Check for collision between the player and the monster
    if player.collidesWith(monster):
        print("Player is Colliding with Monster!")
    #Check for collision between any of the player projectiles and the monster
    if player.projectilesCollideWith(monster):
        print("Projectile Collided with Monster!")
    
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