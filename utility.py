import pygame
import math
import pygame.math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, NAME
class Text():
    def __init__(self, screen, text, color, size, x=0, y=0):
        self.screen = screen
        self.position = [x,y]
        newfont = pygame.font.SysFont("Arial",size,True,False)
        self.text = newfont.render(text,True,color)
    
    def display(self):
        self.screen.blit(self.text, self.position)

    def set_position(self, x, y):
        self.position = [x,y]

class Timer():
    def __init__(self):
        self.startTime = 0

    def start(self):
        self.enabled = True
        self.startTime = pygame.time.get_ticks()
    
    def restart(self): #This is the same as start, but allows for easier reading of code in the main file
        self.enabled = True
        self.startTime = pygame.time.get_ticks()

    def time(self):
        if self.enabled:
            return round((pygame.time.get_ticks() - self.startTime)/1000, 1)
        return 0
    
    def end(self):
        self.enabled = False

class Projectile(pygame.sprite.Sprite):
    '''TODO Projectile Class'''
    def __init__(self, image, position, speed):
        pass

class MouseProjectile(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.image.load("./images/"+image).convert_alpha()
        self.position = pygame.math.Vector2(position[0],position[1])
        xpos,ypos = pygame.mouse.get_pos()
        self.direction = (pygame.math.Vector2(xpos, ypos) - self.position).normalize()
        self.rect = self.image.get_rect()
        #Rotates the projectile towards it's direction
        self.image = pygame.transform.rotate(self.image, -1*math.degrees(math.atan2(self.direction.y, self.direction.x)))
    
    def set_speed(self, speed):
        self.speed = speed

    def move(self):
        velocity = self.direction * self.speed
        self.position += velocity
        
class Character(pygame.sprite.Sprite):
    '''A class for characters in your game'''
    def __init__(self, image, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/"+image).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.position = pygame.math.Vector2(position[0],position[1])
        self.rect = self.image.get_rect()
        self.speed = 10
        self.size = size
        #Accessible positions on the Character
        self.__update_positions()

    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, x, y):
        self.position = pygame.math.Vector2(x,y)
        self.__update_positions()

    def move(self, direction):
        if direction.length() != 0:
            direction = direction.normalize()
            velocity = direction * self.speed
            self.position += velocity
        self.__update_positions()
    
    #Create easy positions for each character
    def __update_positions(self):
        self.rect = self.image.get_rect() #Update the hitbox/rect when the player moves (might not be needed)
        self.center = pygame.math.Vector2(self.position.x + self.rect.width/2, self.position.y + self.rect.height/2)
        self.left = pygame.math.Vector2(self.position.x, self.position.y + self.rect.height/2)
        self.right = pygame.math.Vector2(self.position.x + self.rect.width, self.position.y + self.rect.height/2)
        self.top = pygame.math.Vector2(self.position.x + self.rect.width/2, self.position.y)
        self.bottom = pygame.math.Vector2(self.position.x + self.rect.width/2, self.position.y + self.rect.height)
        self.topleft = pygame.math.Vector2(self.position.x, self.position.y)
        self.topright = pygame.math.Vector2(self.position.x + self.rect.width, self.position.y)
        self.bottomleft = pygame.math.Vector2(self.position.x, self.position.y + self.rect.height)
        self.bottomright = pygame.math.Vector2(self.position.x + self.rect.width, self.position.y + self.rect.height)

class Camera():
    '''Allows use of a camera within a level'''
    def __init__(self):
        #TODO
        pass

class Level():
    '''A class for each level in your game'''
    def __init__(self, screen, background, sprites=[]):
        self.sprites = pygame.sprite.Group() #Sprite Group for every sprite in the level
        self.background = pygame.image.load("./images/"+background).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.projectiles = []
        self.texts = []
        self.screen = screen
        self.cameraEnabled = False
        for sprite in sprites:
            self.sprites.add(sprite)

    def enableCamera(self):
        self.cameraEnabled = True

    def disableCamera(self):
        self.cameraEnabled = False

    def addText(self, text):
        self.texts.append(text)

    def addSprite(self, sprite):
        self.sprites.add(sprite)

    def addProjectile(self, p): #Simple method to add a projectile to the level
        self.projectiles.append(p)

    def display(self): 
        #TODO add in camera logic based
        #Display this levels background
        self.screen.blit(self.background, (0,0))
        #Display every sprite at its own position
        for text in self.texts:
            text.display()
        for sprite in self.sprites:
            self.screen.blit(sprite.image, sprite.position)
        for p in self.projectiles:
            p.move() #Move every projectile
            self.screen.blit(p.image, p.position) #Display each projectile
            #Remove the projectiles if they travel off screen
            if p.position.x> SCREEN_WIDTH or p.position.x < -p.rect.width:
                self.projectiles.remove(p)
            elif p.position.y > SCREEN_HEIGHT or p.position.y < -p.rect.height:
                self.projectiles.remove(p)

class Game():
    def __init__(self, startingLevel): #Begin on the startingLevel
        self.currentLevel = startingLevel
    
    def setLevel(self, level): #Method to transition levels
        self.currentLevel = level
    
    def run(self): #Method to display the current level / run the game
        self.currentLevel.display()