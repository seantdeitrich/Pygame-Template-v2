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

    def setPosition(self, x, y):
        self.position = [x,y]

class Timer():
    def __init__(self):
        self.startTime = 0
        self.enabled = False

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
    
    def timeInMilliseconds(self):
        if self.enabled:
            return pygame.time.get_ticks() - self.startTime
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
        #Surround in a try except to catch File Not Found
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

    #Collision Performance Note:
    #Generally what you will want to do is check if two sprites have colliding rects 
    #Then only if this test is positive do you check the masks.

    def collidesWith(self, other):
        if pygame.sprite.collide_rect(self, other): #If the rectangles are overlapping
            return pygame.sprite.collide_mask(self, other)  #Returns the location relative to the projectile's origin of where the collision occured

class Character(pygame.sprite.Sprite):
    '''A class for characters in your game'''
    def __init__(self, image, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/"+image).convert_alpha()
        self.animated = False #Boolean for whether the character is animated or not
        self.image = pygame.transform.scale(self.image, size) #Scaling to the given size
        self.position = pygame.math.Vector2(position[0],position[1]) #Changing position into a vector
        self.mask = pygame.mask.from_surface(self.image) #Helps improve performance of mask collision, needs to be updated when scaled or on image change
        self.rect = self.image.get_rect() #Acquiring the rectangle around the character
        self.speed = 10 #Speed variable
        self.velocity = pygame.Vector2()
        self.gravityEnabled = False
        self.gravity = 1
        self.fliph = False
        self.flipv = False
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.projectiles = pygame.sprite.Group() #Group to hold all projectiles belonging to this character
        self.currentAnimation = 0 #Number to keep track of which animation is currently being used
        self.animations = [] #Holds all the animations
        #Update accessible positions on the Character
        self.__update_positions()
    
    #Allows flipping the sprite
    #Needs to work for animations as well, and their masks
    #Also, redo the mask for pixel perfect collision after flip
    def flipHorizontal(self, bool):
        if self.fliph != bool:
            if self.animated:
                for animation in self.animations:
                    animation.flipHorizontal()
                self.fliph = bool
            else:    
                self.fliph = bool
                self.image = pygame.transform.flip(self.image, self.fliph, False) #Flip the image
                self.mask = pygame.mask.from_surface(self.image) #Update the mask

    def flipVertical(self, bool):
        if self.flipv != bool: #if there is a difference from how the image is currently flipped
            self.flipv = bool
            self.image = pygame.transform.flip(self.image, False, True) #Flip the image
            self.mask = pygame.mask.from_surface(self.image) #Update the mask

    def enableGravity(self):
        self.gravityEnabled = True

    def disableGravity(self):
        self.gravityEnabled = False

    def addAnimation(self, animation):
        self.animations.append(animation) #Insert the new animation onto the end of the animations list

    def setAnimation(self, animation):
        self.currentAnimation = self.animations.index(animation) #Find the index of the given animation and set it to the currentAnimation 

    def addProjectile(self, p): #Simple method to add a projectile that is owned by the character
        self.projectiles.add(p)

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) #Check to see if the mouse clicked on the character

    def draw(self, screen):
        #If the player is not animated
        if not self.animated: #Put the player on the screen
            screen.blit(self.image, self.position)
        else: #Otherwise put the current animation on the screen
            self.animations[self.currentAnimation].position = self.position
            self.image = self.animations[self.currentAnimation].image
            self.rect = self.animations[self.currentAnimation].rect
            self.animations[self.currentAnimation].draw(screen)
        #Always draw projectiles   
        for p in self.projectiles:
            screen.blit(p.image, p.position) #Display each projectile
            #Remove the projectiles if they travel off screen
            if p.position.x> SCREEN_WIDTH or p.position.x < -p.rect.width:
                self.projectiles.remove(p)
            elif p.position.y > SCREEN_HEIGHT or p.position.y < -p.rect.height:
                self.projectiles.remove(p)
            p.move() #Move each projectile by it's assigned velocity

    def drawMask(self):
        olist = self.mask.outline()
        pygame.draw.lines(self.image,(255, 255, 255),True,olist)

    def setSpeed(self, speed):
        self.speed = speed

    def setPosition(self, position):
        self.position = position
        self.__update_positions()

    def move(self, direction):
        if direction.length() != 0: #If the player has a direction
            direction = direction.normalize() #Normalize the direction
            self.velocity = direction * self.speed #Multiply by speed
            self.position += self.velocity #Shift the players position by the calculated velocity
            self.__update_positions() #Anytime the character moves, update the rectangle and positions as well


    def moveWithSpeed(self, direction, speed):
        if direction.length() != 0: #If the player has a direction
            direction = direction.normalize() #Normalize the direction
            velocity = direction * speed #Multiply by speed
            self.position += velocity #Shift the players position by the calculated velocity
        self.__update_positions() #Anytime the character moves, update the rectangle and positions as well
    
    #Collision Performance Note:
    #Generally what you will want to do is check if two sprites have colliding rects 
    #Then only if this test is positive do you check the masks.

    def collidesWith(self, other):
        #The collide mask function allows for pixel perfect collision without performance hits
        if pygame.sprite.collide_rect(self, other):
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
        self.mask = pygame.mask.from_surface(self.image) #Helps improve performance of mask collision, needs to be updated when scaled or on image change

class Camera():
    '''Allows use of a camera within a level'''
    def __init__(self):
        #TODO
        pass

class Level():
    '''A class for each level in your game'''
    def __init__(self, screen, background, sprites=[]):
        self.sprites = pygame.sprite.Group() #Sprite Group for every sprite in the level
        #Surround in a try except to catch File Not Found
        self.background = pygame.image.load("./images/"+background).convert()
        #
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

class Animation():
    #Note that spritesheets must be a single row
    def __init__(self, spritesheet, rows, cols, fps=12):
        self.spritesheet = pygame.image.load("./images/"+spritesheet).convert_alpha() #Load the spritesheet in and allow for transparency
        self.position = pygame.Vector2() #This should be inherited from the parent, might need to adjust later
        self.frames = [] #Container for each frame from the spritesheet
        self.masks = [] #Container for each frame's mask to maintain pixel perfect collision
        self.currentFrame = 0 #Keeps track of which frame we're at in the spritesheet
        self.rows = rows 
        self.cols = cols
        self.totalFrames = self.rows*self.cols #Calculating total amount of frames
        self.frameWidth = self.spritesheet.get_width()/cols #Calculating width of a single frame
        self.frameHeight = self.spritesheet.get_height()/rows #Calculating height of a single frame
        self.frameTime = 1000/fps #This is the amount of time that a frame will play for
        self.timer = Timer()
        self.timer.start()
        self.splitSpriteSheet() #Populates frames list with each individual frame from the sheet
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def splitSpriteSheet(self): #Used to populate the frames list with individual frames from the sheet
        #Go through each row and column
        for row in range(self.rows):
            for col in range(self.cols):
                #Adjust the starting location
                x = col * self.frameWidth
                y = row * self.frameHeight
                #Create the appropriate rectangle to cut out of the spritesheet
                frameRect = pygame.Rect(x, y, self.frameWidth, self.frameHeight) 
                frame = self.spritesheet.subsurface(frameRect)
                self.frames.append(frame)
                self.masks.append(pygame.mask.from_surface(frame))
    
    def flipHorizontal(self):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.flip(self.frames[i], True, False)
            

    def draw(self, screen):
        screen.blit(self.image, self.position)
        #If the correct amount of time has passed
        if self.timer.timeInMilliseconds() > self.frameTime:
            #Advance to the next frame in the animation
            self.currentFrame += 1
            self.timer.restart() #Restart the timer after we advance a frame
            #Loop back to the first frame if we've played the whole animation
            if self.currentFrame >= self.totalFrames:
                self.currentFrame = 0
        self.image = self.frames[self.currentFrame]
        self.rect = self.image.get_rect()
        #self.drawMask()

    def drawMask(self): #Debug Purposes
        olist = pygame.mask.from_surface(self.image).outline()
        pygame.draw.lines(self.image,(255, 255, 255),True,olist)

    def scale(self):
        pass