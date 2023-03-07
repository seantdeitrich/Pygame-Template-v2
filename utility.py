import pygame
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
        self.position = (x,y)
        self.rect = self.image.get_rect()
    
    def set_position(self, x, y):
        self.position = (x,y)
        self.rect = self.image.get_rect()
    
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
        self.screen = screen
        for sprite in sprites:
            self.sprites.add(sprite)

    def display(self):
        #Display this levels background
        self.screen.blit(self.background, (0,0))
        #Display every sprite at its own position
        for sprite in self.sprites:
            self.screen.blit(sprite.image, sprite.position)
    
class Game():
    def __init__(self, startingLevel):
        self.currentLevel = startingLevel
    
    def switchTo(self, level):
        self.currentLevel = level
    
    def run(self):
        self.currentLevel.display()
        self.currentLevel.input()

    def display(self):
        self.currentLevel.display()

    def process(self, events):
        pass