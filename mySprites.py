'''Anders Tai

   May 27, 2019
   
   Classic Minesweeper Sprites
'''

import pygame

class Tile(pygame.sprite.Sprite):
    '''This sprite is the basic tile sprite that can be reconfigured to act as a bomb'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        #loading needed images 
        self.undiscovered = pygame.image.load("Images/undiscovered.png")
        self.discovered = pygame.image.load('Images/discovered.png')
        self.flag = pygame.image.load('Images/flag.png')
        
        #Various variables for the logic of the game
        self.image = self.undiscovered
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y        
        
        self.discoveredFlag = False
        self.flagged = False
        self.checked = False
        self.value = 0
        self.flagCount = 0
        self.lost = False
        self.reveal = False
        
    def setFlag(self):
        '''This function sets the tile to flagged'''
        if not self.discoveredFlag:
            self.image = self.flag
            self.flagged = True
        
    def setUnFlag(self):
        '''This function unflagges the tile'''
        if not self.discoveredFlag:
            self.image = self.undiscovered
            self.flagged = False

    def setReveal(self):
        '''This function reveals the tile'''
        if not self.flagged and not self.discoveredFlag:
            if self.value == -1:
                self.image = pygame.image.load('Images/mineClick.png')
            elif self.value == 0:
                self.image = self.discovered 
            elif self.value == 1:
                self.image = pygame.image.load('Images/one.png')
            elif self.value == 2:
                self.image = pygame.image.load('Images/two.png')
            elif self.value == 3:
                self.image = pygame.image.load('Images/three.png')
            elif self.value == 4:
                self.image = pygame.image.load('Images/four.png')
            elif self.value == 5:
                self.image = pygame.image.load('Images/five.png')
            elif self.value == 6:
                self.image = pygame.image.load('Images/six.png')
            elif self.value == 7:
                self.image = pygame.image.load('Images/seven.png')
            elif self.value == 8:
                self.image = pygame.image.load('Images/eight.png')
        
            self.discoveredFlag = True
            
            if self.value == -1:
                self.lost = True
        
    def addMine(self):
        '''This function add one to the value of the tile'''
        if self.value != -1:
            self.value += 1
            
    def addFlagCount(self, value):
        '''This function add a certian value to the number of mines flagged around the tile'''
        self.flagCount += value
        
    def gameEnd(self):
        '''This function is just used to set the tile to the endGame mode'''
        if self.value == -1 and not self.flagged and not self.discoveredFlag:
            self.image = pygame.image.load('Images/mine.png')
        if self.value != -1 and self.flagged and not self.discoveredFlag:
            self.image = pygame.image.load('Images/mineWrong.png')        
            
class HappyFace(pygame.sprite.Sprite):
    '''This is the Happy Face sprite in the middle of the screen'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #Load needed images
        self.scared = pygame.image.load("Images/happyO.png")
        self.happy = pygame.image.load('Images/happy.png')
        self.click = pygame.image.load('Images/click.png')
        self.cool = pygame.image.load('Images/cool.png')
        self.dead = pygame.image.load('Images/dead.png')
        #Set needed variables
        self.image = self.happy
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        
    def setScared(self):
        '''this function sets the image to scared :o'''
        self.image = self.scared
        
    def setNormal(self):
        '''This function sets the image back to normal'''
        self.image = self.happy
        
    def setClick(self):
        '''This function sets the image as if the button is clicked'''
        self.image = self.click
        
    def setWin(self):
        '''This function sets the image if you won'''
        self.image = self.cool
        
    def setLost(self):
        '''This function sets the image if you lost'''
        self.image = self.dead
        
class Counter(pygame.sprite.Sprite):
    '''This is both the mine counter (top left) and the time counter (top right)'''
    def __init__(self, n, x, y):
        pygame.sprite.Sprite.__init__(self)
        #Loading all of the number 0-9 including the -
        self.numbers = [pygame.image.load("Images/0.png"), pygame.image.load("Images/1.png"), pygame.image.load("Images/2.png"), pygame.image.load("Images/3.png"), pygame.image.load("Images/4.png"), pygame.image.load("Images/5.png"), pygame.image.load("Images/6.png"), pygame.image.load("Images/7.png"), pygame.image.load("Images/8.png"), pygame.image.load("Images/9.png"), pygame.image.load("Images/-.png")]
        
        #Setting needed variables
        self.mines = n
        self.x = x
        self.y = y
        
        self.ones = 0
        self.tens = 0
        self.hundreds = 0
        
        self.image = pygame.Surface((75, 44))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        
    def add(self):
        '''This function adds one to the value of the counter'''
        if self.mines < 999:
            self.mines += 1            
        
    def minus(self):
        '''This function minuses one to the value of the counter'''
        if self.mines > -99:
            self.mines -= 1
            
    def end(self):
        '''Sets the value to 0'''
        self.mines = 0
    
    def update(self):
        '''This function loads the proper image depending on the value'''
        self.ones = 0
        self.tens = 0
        self.hundereds = 0
        
        if self.mines < 0:
            self.hundreds = 10
            if len(str(self.mines)) == 2:
                self.ones = int(str(self.mines)[1])
            elif len(str(self.mines)) == 3:
                self.tens = int(str(self.mines)[1])
                self.ones = int(str(self.mines)[2])
    
        else:
            self.hundreds = 0
            if len(str(self.mines)) == 1:
                self.ones = self.mines
                
            elif len(str(self.mines)) == 2:
                self.tens = int(str(self.mines)[0])
                self.ones = int(str(self.mines)[1])
                
            elif len(str(self.mines)) == 3:
                self.ones = int(str(self.mines)[2])
                self.tens = int(str(self.mines)[1])
                self.hundreds = int(str(self.mines)[0])
                
        self.image.blit(self.numbers[self.hundreds], (0,0))
        self.image.blit(self.numbers[self.tens], (25,0))
        self.image.blit(self.numbers[self.ones], (50,0))

class Ghost(pygame.sprite.Sprite):
    '''This sprite is the preclick sprite'''
    def __init__(self, size, board, offSet):
        pygame.sprite.Sprite.__init__(self)
        #Load singular image
        self.discovered = pygame.image.load('Images/discovered.png')
        self.active = False
        self.board = board
        
        self.tileSize = 30
        self.yOffSet = 98
        self.xOffSet = 19
        self.boardSize = size
        self.image = self.discovered
        self.offSet = offSet
        self.rect = self.image.get_rect()
        
        self.rect.center = (-500,-500)
                
    def updateBoard(self, board):
        '''Updates the board version in the sprite'''
        self.board = board
                              
    def activate(self):
        '''Activates the ghost'''
        self.active = True

    def deActivate(self):
        '''deActivates the ghost'''
        self.active = False
        self.rect.center = (-500,-500)
        
    def update(self):
        '''Updates the position of the ghost depending on the position of the mouse'''
        if self.active:
            x, y = pygame.mouse.get_pos()
            x = (x-self.xOffSet)//self.tileSize
            y = (y-self.yOffSet)//self.tileSize
            x += self.offSet[0]
            y += self.offSet[1]
                
            if x in range(self.boardSize[0]):
                if y in range(self.boardSize[1]):
                    self.rect.center = (self.xOffSet + x*self.tileSize + 15, self.yOffSet + y*30 + 15)
                    if self.board[y][x].discoveredFlag or self.board[y][x].flagged:
                        self.rect.center = (-500,-500)
                        
class StartSprite(pygame.sprite.Sprite):
    '''Starting sprite displaying the different difficultys depending on mouse position'''
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        #Loading fonts
        self.font = pygame.font.Font("American Captain.ttf", 70)
        self.font2 = pygame.font.Font("American Captain.ttf", 60)
        self.screen = screen
    
    def update(self):
        '''Updates the text and position depending on the mouse position'''
        x , y = pygame.mouse.get_pos()
        x = x//30
        #Easy position
        if x < 10:
            self.image = pygame.image.load('Images/background.png')
            message = 'Beginner'
            text = self.font.render(message, 1, (0,0,0))
            self.image.blit(text, (45, 130))
            message = '10 Mines'
            text = self.font.render(message, 1, (0,0,0))
            self.image.blit(text, (50, 280))
            
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)
        #Medium position
        if 9 < x < 20:
            self.image = pygame.image.load('Images/background.png')
            message = 'Intermediate'
            text = self.font2.render(message, 1, (0,0,0))
            self.image.blit(text, (20, 130))
            message = '40 Mines'
            text = self.font.render(message, 1, (0,0,0))
            self.image.blit(text, (50, 280))
            
            self.rect = self.image.get_rect()
            self.rect.topleft = (300,0)
        #Expert position
        if x > 19:
            self.image = pygame.image.load('Images/background.png')
            message = 'Expert'
            text = self.font.render(message, 1, (0,0,0))
            self.image.blit(text, (70, 130))
            message = '99 Mines'
            text = self.font.render(message, 1, (0,0,0))
            self.image.blit(text, (50, 280))
            
            self.rect = self.image.get_rect()
            self.rect.topleft = (600, 0)