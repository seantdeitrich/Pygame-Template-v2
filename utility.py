import pygame
import math
import pygame.math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
class Text():
    def __init__(self, screen, text, color, size, x=0, y=0):
        self.screen = screen
        self.position = [x,y]
        newfont = pygame.font.SysFont("Arial",size,True,False)
        self.text = newfont.render(text,True,color)
    
    def draw(self):
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
    
    def stop(self):
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
        self.mask = pygame.mask.from_surface(self.image) #Helps improve performance of mask collision, needs to be updated when scaled or on image change
        
    def set_speed(self, speed):
        self.speed = speed

    def move(self):
        velocity = self.direction * self.speed
        self.position += velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def collidesWith(self, other):
        return pygame.sprite.collide_mask(self, other)  #Returns the location relative to the projectile's origin of where the collision occured

class Character(pygame.sprite.Sprite):
    '''A class for characters in your game'''
    def __init__(self, image, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/"+image).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.position = pygame.math.Vector2(position[0],position[1])
        self.mask = pygame.mask.from_surface(self.image) #Helps improve performance of mask collision, needs to be updated when scaled or on image change
        self.rect = self.image.get_rect()
        self.speed = 10
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.projectiles = pygame.sprite.Group()
        #Accessible positions on the Character
        self.__update_positions()
    
    def addProjectile(self, p): #Simple method to add a projectile that is owned by the character
        self.projectiles.add(p)

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) #Check to see if the mouse clicked on the character

    def draw(self, screen):
        screen.blit(self.image, self.position)
        for p in self.projectiles:
            screen.blit(p.image, p.position) #Display each projectile
            #Remove the projectiles if they travel off screen
            if p.position.x> SCREEN_WIDTH or p.position.x < -p.rect.width:
                self.projectiles.remove(p)
            elif p.position.y > SCREEN_HEIGHT or p.position.y < -p.rect.height:
                self.projectiles.remove(p)
            p.move()

    def setSpeed(self, speed):
        self.speed = speed

    def set_position(self, x, y):
        self.position = pygame.math.Vector2(x,y)
        self.__update_positions()

    def move(self, direction):
        if direction.length() != 0: #If the player has a direction
            direction = direction.normalize() #Normalize the direction
            velocity = direction * self.speed #Multiply by speed
            self.position += velocity #Shift the players position by the calculated velocity
        self.__update_positions() #Anytime the character moves, update the rectangle and positions as well
    
    def collidesWith(self, other):
        #The collide mask function allows for pixel perfect collision without performance hits
        return pygame.sprite.collide_mask(self, other)  #Returns the location relative to the character's origin of where the collision occured

    def projectilesCollideWith(self, other):
        for p in self.projectiles:
            if p.collidesWith(other):
                p.kill() #Remove the projectile when it collides with other
                return True #Return True because a collision occured
    
    #Create easy positions for each character
    def __update_positions(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
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

    def add(self, sprite):
        self.sprites.add(sprite)

    def display(self): 
        #TODO add in camera logic based
        #Display this levels background
        self.screen.blit(self.background, (0,0))
        #Draw all text to the screen (necessary because text isn't a sprite)
        for text in self.texts:
            text.draw()
        #Draw all sprites to the screen
        for sprite in self.sprites:
            sprite.draw(self.screen) 

class Game():
    def __init__(self, startingLevel): #Begin on the startingLevel
        self.currentLevel = startingLevel
    
    def setLevel(self, level): #Method to transition levels
        self.currentLevel = level
    
    def run(self): #Method to display the current level / run the game
        self.currentLevel.display()

class Sound(pygame.mixer.Sound):
    #Since this class extends the pygame Sound class, we have access to the following methods:
    #play(), stop(), fadeout(), set_volume(), get_volume()
    def __init__(self, filename):
        pygame.mixer.Sound.__init__(self, "./sounds/"+filename)
    def loop(self):
        self.play(-1)
    #Made this for naming consistency on all methods
    def setVolume(self, volume):
        self.set_volume(volume)
    def getVolume(self):
        return self.get_volume()
    #Don't forget about the fadeout method, which could be useful in each game
    