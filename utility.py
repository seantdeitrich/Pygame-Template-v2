import pygame
import pygame.math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_NAME, NAME
class Projectile(pygame.sprite.Sprite):
    '''TODO Projectile Class'''
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)        
        self.position = position
        self.direction = direction

class Block(pygame.sprite.Sprite):
    '''Debugging Block Class'''
    def __init__(self, color, width, height, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.position = pygame.math.Vector2(x,y)
        self.rect = self.image.get_rect()
        self.speed = 10
    
    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, x, y):
        self.position = pygame.math.Vector2(x,y)
        self.rect = self.image.get_rect()
    
    def move(self, direction):
        if direction.length() != 0:
            direction = direction.normalize()
            velocity = direction * self.speed
            self.position += velocity

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

class Character(pygame.sprite.Sprite):
    '''A class for each character in your game'''
    def __init__(self, image, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/"+image).convert_alpha()
        self.position = (x,y)
        self.rect = self.image.get_rect()

class Camera():
    def __init__(self):
        pass

class Level():
    '''A class for each level in your game'''
    def __init__(self, screen, background, sprites):
        self.sprites = pygame.sprite.Group()
        self.background = pygame.image.load("./images/"+background).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = screen
        for sprite in sprites:
            self.sprites.add(sprite)

    def display(self): 
        #Display this levels background
        self.screen.blit(self.background, (0,0))
        #Display every sprite at its own position
        for sprite in self.sprites:
            self.screen.blit(sprite.image, sprite.position)
    
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

class Game():
    def __init__(self, startingLevel):
        self.currentLevel = startingLevel
    
    def setLevel(self, level):
        self.currentLevel = level
    
    def run(self):
        self.currentLevel.display()