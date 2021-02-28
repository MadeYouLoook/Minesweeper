'''Anders Tai

   May 27, 2019
   
   Classic Minesweeper Game
'''

# I - Import and Initialize
import pygame, mySprites, random
pygame.init()
pygame.mixer.init()

#CONSTANTS TABLE OF VALUES
#constant[0] tileSize
#constant[1] yOffSet
#constant[2] xOffSet
#constant[3] boardSize 
#constant[4] backgroundImage
#constant[5] numberMines
#constant[6] screenSize

def main():
    '''This function is the main loop that cycles between my start and game screens'''
    quitGame = False
    while not quitGame:
        #Constants is just a list of numbers that are needed frequently and are used to make an adjustable board
        quitGame, constant = startScreen()
        if not quitGame:
            mainGame(constant)
    pygame.quit()

def startScreen():  
    '''This is the start screen for my game where you pick the size/difficulty of the game'''   
    # Display
    screen = pygame.display.set_mode((900, 480))   
    pygame.display.set_caption("Pick a size!")
    
    # Entities
    background = pygame.Surface(screen.get_size())
    screen.blit(background, (0, 0))
    
    pygame.mixer.music.load("sounds/mainmenu.ogg")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    click = pygame.mixer.Sound("sounds/click.wav")
    click.set_volume(0.5)    
    
    #Creating constant list
    tileSize = 30
    yOffSet = 98
    xOffSet = 19
    boardSize = (30,16)
    backgroundImage = 'Images/30x16.png'
    numberMines = 99 
    screenSize = (xOffSet*2+tileSize*boardSize[0], xOffSet+yOffSet +tileSize*boardSize[1])
    constant = [tileSize, yOffSet, xOffSet, boardSize, backgroundImage, numberMines, screenSize]
    
    #Tiles just for show in the background
    tiles = []
    for y in range (0 ,constant[0]*constant[3][1], constant[0]):
        row = []
        for x in range (0, constant[0]*constant[3][0], constant[0]):
            tile = mySprites.Tile(x, y)
            row.append(tile)
        tiles.append(row)
    
    #The sprite that follows the mouse displaying the different difficultys    
    start = mySprites.StartSprite(screen)
    
    allSprites = pygame.sprite.OrderedUpdates(tiles, start)
    
    # ACTION
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                keepGoing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True
                    keepGoing = False
                                        
            elif event.type == pygame.MOUSEBUTTONUP:
                #LEFT MOUSE UP
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    pos = getPosition((x+19,y+98), constant)
                    #All of the different difficultys and their needed variables
                    if pos:
                        x, y = pos
                        if x in range(10):
                            boardSize = (9,9)
                            backgroundImage = 'Images/9x9.png'
                            numberMines = 10
                            screenSize = (xOffSet*2+tileSize*boardSize[0], xOffSet+yOffSet +tileSize*boardSize[1])
                        elif x in range(10,20):
                            boardSize = (16,16)
                            backgroundImage = 'Images/16x16.png'
                            numberMines = 40
                            screenSize = (xOffSet*2+tileSize*boardSize[0], xOffSet+yOffSet +tileSize*boardSize[1])
                        else:
                            boardSize = (30,16)
                            backgroundImage = 'Images/30x16.png'
                            numberMines = 99
                            screenSize = (xOffSet*2+tileSize*boardSize[0], xOffSet+yOffSet +tileSize*boardSize[1])
                        constant = [tileSize, yOffSet, xOffSet, boardSize, backgroundImage, numberMines, screenSize]
                        #Return False as you dont want to quit and return the constants
                        click.play()
                        return False, constant
                    
        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    return quit, constant
        
def mainGame(constant):
    '''This function defines the 'mainline logic' for our game.'''   
    # Display
    screen = pygame.display.set_mode(constant[6])
    #Set display caption according to the size of the screen
    if constant[6] == (308,387):
        pygame.display.set_caption("Minesweeper! (Beginner)")
    elif constant[6] == (518,597):
        pygame.display.set_caption("Minesweeper! (Intermediate)")
    elif constant[6] == (938,597):
        pygame.display.set_caption("Minesweeper! (Expert)")            
    
    # Entities
    background = pygame.Surface(screen.get_size())
    background = pygame.image.load(constant[4])
    screen.blit(background, (0, 0))
    
    #Import needed sound effects
    pygame.mixer.music.load("sounds/mainmenu.ogg")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    click = pygame.mixer.Sound("sounds/click2.wav")
    click.set_volume(0.5)
    flag = pygame.mixer.Sound("sounds/flag2.wav")
    flag.set_volume(0.5)
    unflag = pygame.mixer.Sound("sounds/unflag.wav")
    unflag.set_volume(0.5)
    wrong = pygame.mixer.Sound("sounds/wrong.wav")
    wrong.set_volume(0.5)
    gameWin = pygame.mixer.Sound("sounds/gameWin.ogg")
    gameWin.set_volume(0.5)
    gameOver = pygame.mixer.Sound("sounds/gameOver.ogg")
    gameOver.set_volume(0.5) 
    
    #Tiles
    tiles, mines = makeBoard(constant)
    #Sprite that appears when you click down (single or double), preclick image.
    ghost = mySprites.Ghost(constant[3], tiles, (0,0))
    ghosts = []
    for x in range(-1,2):
        for y in range(-1,2):
            tile = mySprites.Ghost(constant[3], tiles, (x,y))
            ghosts.append(tile)
            
    happyFace = mySprites.HappyFace((constant[6][0]-50)//2, (constant[1]-50)//2)
    mineText = mySprites.Counter(constant[5], 30, 26)
    timer = mySprites.Counter(0, screen.get_width()-105, 26)
    
    allSprites = pygame.sprite.OrderedUpdates(tiles, happyFace, mineText, timer, ghost, ghosts)
    
    # ACTION
    # Assign 
    clock = pygame.time.Clock()
    
    keepGoing = True
    wonGame = None 
    timing = False
    happyDown = False
    endGame = False
    resetGame = False
    doubleClick = False
    
    # Loop
    while keepGoing:
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    
                elif event.key == pygame.K_SPACE:
                    #Space acts and a left and right click
                    pos = getPosition(pygame.mouse.get_pos(), constant)
                    #!= 'happy' just means not the happy face button
                    if pos and pos != 'happy':
                        #If the tile is not discovered
                        if not tiles[pos[1]][pos[0]].discoveredFlag:
                            if not endGame:
                                flag.play()
                                #Calls extra method at bottom to flag mine and add to a counter for all of the tiles around (for logic later)
                                flagTile(tiles, mineText, constant)
                        #If the tile is discovered
                        else:
                            x, y = pos
                            
                            if tiles[y][x].flagCount == tiles[y][x].value and tiles[y][x].discoveredFlag:
                                #Reveal around just puts off a switch that says to reveal then revealEmptyGroup actually reveals it
                                revealAround(tiles, (y,x), constant)
                            revealEmptyGroup(tiles, constant)
                    #Check if game is lost/won
                    wonGame = checkWin(tiles, constant)
            
            #Special event that adds one to the counter every second                    
            elif event.type == pygame.USEREVENT:
                if not endGame:
                    #If already timing
                    if timing:
                        timer.add()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = pygame.mouse.get_pressed()
                #Left and right mouse button down
                if (mousePressed[0] and mousePressed[2]):
                    if not endGame:
                        pos = getPosition(pygame.mouse.get_pos(), constant)
                        if pos and pos != 'happy':
                            #Activate the 3x3 preclick sprite
                            for tile in ghosts:
                                tile.activate()
                            doubleClick = True
                            
                #Right mouse button down  
                elif mousePressed[2]:
                    if not endGame:
                        pos = getPosition(pygame.mouse.get_pos(), constant)
                        flag.play()
                        #Flag tile
                        flagTile(tiles, mineText, constant)
                    
                #Left mouse button down                     
                elif mousePressed[0]:
                    pos = getPosition(pygame.mouse.get_pos(), constant)
                    if not endGame:
                        if pos and pos != 'happy':
                            happyDown = True
                            #Activate the 1x1 preclick sprite
                            ghost.activate()
                            #Change the happy face image
                            happyFace.setScared()
                    #If click the happy face        
                    if pos == 'happy':
                        happyDown = True
                        #Change the happy face image to clicked
                        happyFace.setClick()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                #Left and right mouse button up
                if doubleClick:
                    if not endGame:
                        pos = getPosition(pygame.mouse.get_pos(), constant)
                        if pos and pos != 'happy':
                            x, y = pos
                            #Reveal around if number flagged around is equal to the value displayed
                            if tiles[y][x].flagCount == tiles[y][x].value and tiles[y][x].discoveredFlag:
                                revealAround(tiles, (y,x), constant)
                            revealEmptyGroup(tiles, constant)
                        #Deactivate the preclick sprite   
                        for tile in ghosts:
                            tile.deActivate() 
                        doubleClick = False
                        #Check if you won/lost
                        wonGame = checkWin(tiles, constant)
                        
                #Left mouse button up 
                elif event.button == 1:
                    pos = getPosition(pygame.mouse.get_pos(), constant)
                    if pos and pos != 'happy' and not endGame:
                        x, y = pos
                        #Click for the first time, not already timing
                        if not timing:
                            #Activate timer
                            pygame.time.set_timer(pygame.USEREVENT, 1000)
                            #First move cant hit a bomb
                            tiles, mines = firstMove(tiles, mines, pos, constant)
                            #Update board variable in the preclick Sprite
                            ghost.updateBoard(tiles)
                            for tile in ghosts:
                                tile.updateBoard(tiles)
                            allSprites = pygame.sprite.OrderedUpdates(tiles, happyFace, mineText, timer, ghost, ghosts)
                            timing = True
                        #Play sound effect
                        if tiles[y][x].discoveredFlag == False:
                            click.play()
                            #Reveal the one tile
                        tiles[y][x].setReveal()
                        #If value is 0, the tile is empty, reveal tile around
                        if tiles[y][x].value == 0:            
                            revealAround(tiles, (y,x), constant)       
                        revealEmptyGroup(tiles, constant)
                        
                        #Check if you won and make happy face normal
                        happyFace.setNormal()
                        wonGame = checkWin(tiles, constant)
                            
                    #If they clicked happy face    
                    if pos == 'happy':
                        click.play()
                        #reset game
                        resetGame = True
                #Make happy face normal        
                ghost.deActivate()
                if happyDown:
                    happyFace.setNormal()
                    happyDown = False
        #Reset the game            
        if resetGame:
            #Reset all flags/switches
            timing, resetGame, endGame, wonGame = False, False, False, None
            #Make new board
            tiles, mines = makeBoard(constant)
            ghost.updateBoard(tiles)
            for tile in ghosts:
                tile.updateBoard(tiles)                
            numberFlagged = constant[5]
            mineText.mines = 0
            timer.mines = 0
            mineText = mySprites.Counter(constant[5], 30, 26)
            timer = mySprites.Counter(0, screen.get_width()-105, 26)
            
            allSprites = pygame.sprite.OrderedUpdates(tiles, happyFace, mineText, timer, ghost, ghosts)
            
        #If both left and right are down and the mouse is moved off screen   
        if doubleClick:
            pos = getPosition(pygame.mouse.get_pos(), constant)
            if not pos and pos != 'happy':
                for tile in ghosts:
                    tile.deActivate()  
        
        #If you lost the game           
        if wonGame == False:
            gameOver.play()
            happyFace.setLost()
            gameLost(tiles, constant)
            wonGame, endGame = None, True
            
        #If you won the game
        elif wonGame:
            gameWin.play()            
            for cord in mines:
                x, y = cord
                tiles[y][x].setFlag()
            happyFace.setWin()
            mineText.end()
            wonGame, endGame = None, True

        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
                 
        pygame.display.flip()
    
def getPosition(mousePos, constant):
    '''This function takes in the mouse position and constants. It returns the index of the tile in the nested list that the tiles are stored in'''
    x, y = mousePos
    #If the mouse clicked on happy face
    if constant[2]-1 < y < constant[2]+51:
        if (((constant[6][0]-50)//2)-1) < x < (((constant[6][0]-50)//2)+51):
            return 'happy'
    #If mouse is on the border
    if x < constant[2] or x > constant[0]*constant[3][0] + constant[2]:
        return None
    if y < constant[1] or y > constant[0]*constant[3][1] + constant[1]:
        return None
    #Return the index
    else:
        x = (x-constant[2])//constant[0]
        y = (y-constant[1])//constant[0]
        return ((x,y))
    
def makeBoard(constant):
    '''This function makes the nested list for all my tiles and makes a list containing all of the indexes of the mines. While taking in the constants'''
    #The whole board
    tiles = []
    for y in range (constant[1], constant[0]*constant[3][1] + constant[1], constant[0]):
        #Each row created depending on the constant
        row = []
        for x in range (constant[2], constant[0]*constant[3][0] + constant[2], constant[0]):
            tile = mySprites.Tile(x, y)
            row.append(tile)
        tiles.append(row)
    #Make the mines of the board
    mines = [] 
    #Constant 5 is the number of mines
    for i in range(constant[5]):
        while True:
            #Create a random not already created mine
            x = random.randint(0,constant[3][0]-1)
            y = random.randint(0,constant[3][1]-1)
            cord = (x,y)
            if cord not in mines:
                break
        mines.append(cord)
        tiles[y][x].value = -1
    #Set up the board, creating the right values (Displayed number)    
    boardSetup(tiles, mines, constant)
    return tiles, mines

def firstMove(board, mines, pos, constant):
    '''This function takes in the board, all of the mine positions, the mouse position, and constants. This function ensures that you will always click on an open square during your first click, kick starting the game'''
    #Safe squares (Squares that cant have a mine), change suqares (squares that are to be changed), and a counter for how many new mines to be added
    safe = []
    change = []
    counter = 0
    #Removing mines from a 3x3 area around the click, counting how many mines are removed and adding each square in the 3x3 to the safe list
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            if -1 < y < constant[3][1] and -1 < x < constant[3][0]:
                safe.append((x, y))
                if board[y][x].value == -1:
                    counter += 1
                    mines.remove((x, y))
                    for x2 in range(x-1, x+2):
                        for y2 in range(y-1, y+2):
                            if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                                if board[y2][x2].value not in [-1,0]:
                                    board[y2][x2].value -= 1
                board[y][x].value = 0
    #Reseting up those new squares in the 3x3        
    for x in range(pos[0]-1, pos[0]+2):
        for y in range(pos[1]-1, pos[1]+2):
            for x2 in range(x-1, x+2):
                for y2 in range(y-1, y+2):
                    if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                        if board[y2][x2].value == -1:
                            if -1 < y < constant[3][1] and -1 < x < constant[3][0]:
                                board[y][x].value += 1
    #Creating new mines that arent already created and arent in the safe zone                    
    for i in range(counter):
        while True:
            x = random.randint(0,constant[3][0]-1)
            y = random.randint(0,constant[3][1]-1)
            cord = (x,y)
            if cord not in mines and cord not in safe:
                break
        mines.append(cord)
        board[y][x].value = -1
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                    if board[y2][x2].value != -1:
                        board[y2][x2].value += 1        
    
    return board, mines    
    
def boardSetup(board, mines, constant):
    '''This function takes in the board, the mine positions, constants for the game. This function creates the value of each square depending on the number of mines beside it'''
    for cord in mines:
        x, y = cord
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                    board[y2][x2].addMine()  
                
def revealAround(board, minePos, constant):
    '''This function takes in the board, the tile index, and the constants. This function reveals all of the tiles around of the given position'''
    click = pygame.mixer.Sound("sounds/click2.wav")
    click.set_volume(0.5)
    play = False
    y, x = minePos
    for x2 in range(x-1, x+2):
        for y2 in range(y-1, y+2):
            if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                board[y2][x2].setReveal()
                if board[y2][x2].discoveredFlag == False:
                    play = True
                if board[y2][x2].value == 0:
                    checkBeside(board,(y2,x2), constant)
    if play:
        click.play()
                
def checkBeside(board, minePos, constant):
    '''This function takes in the board, the tile index, and the constants. This function checks if any of the tiles beside the given on are empty'''
    y, x = minePos
    for x2 in range(x-1, x+2):
        for y2 in range(y-1, y+2):
            if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                if board[y2][x2].value == 0 and not board[y2][x2].checked:
                    board[y2][x2].reveal = True
                    board[y2][x2].checked = True
                    checkBeside(board,(y2,x2), constant)               
                    
def checkWin(board, constant):
    '''This function takes in the board and constants. This functions checked if you have won the game or lost'''
    for x in range(constant[3][0]):
        for y in range(constant[3][1]):        
            if board[y][x].lost:
                return False
          
    for x in range(constant[3][0]):
        for y in range(constant[3][1]):        
            if board[y][x].flagged and board[y][x].value != -1:
                return None
            elif not board[y][x].discoveredFlag and board[y][x].value != -1:
                return None  
    return True

def revealEmptyGroup(board, constant):
    '''This function takes in board and constants. This function reveals any tiles that are set to be revealed by the check beside function'''
    revealed = False
    click = pygame.mixer.Sound("sounds/click2.wav")
    click.set_volume(0.5)    
    for x in range(constant[3][0]):
        for y in range(constant[3][1]):        
            if board[y][x].reveal:
                revealAround(board, (y,x), constant)
                board[y][x].reveal = False
                
def flagTile(board, mineText, constant):
    '''This function takes in the board and constants and flags the given tile'''
    pos = getPosition(pygame.mouse.get_pos(), constant)
    if pos and pos != 'happy':
        x, y = pos
        try:
            if board[y][x].flagged:
                board[y][x].setUnFlag()
                mineText.add()
                if not board[y][x].discoveredFlag:
                    for x2 in range(x-1, x+2):
                        for y2 in range(y-1, y+2):  
                            if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                                if board[y2][x2].flagCount > 0:
                                    board[y2][x2].addFlagCount(-1)
            else:
                if not board[y][x].discoveredFlag:
                    board[y][x].setFlag()
                    mineText.minus()
                    for x2 in range(x-1, x+2):
                        for y2 in range(y-1, y+2):
                            if -1 < y2 < constant[3][1] and -1 < x2 < constant[3][0]:
                                board[y2][x2].addFlagCount(1) 
        except IndexError:
            pass    

def gameLost(board, constant):
    '''This function takes in the board and constants. This function just changes the board images for when the game is lost'''
    for x in range(constant[3][0]):
        for y in range(constant[3][1]):        
            board[y][x].gameEnd()
        
# Call the main function
main()