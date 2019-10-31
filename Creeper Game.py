from creeperLocationRandomizer import generateRandomCreeperLocations

import random, sys, time, pygame, os
from pygame.locals import *

import pprint

workingDir = r'C:\Come On Python Games\resources'
os.chdir(workingDir)

baseImagePath = (r'.\creeperGame')

FPS = 30
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768

BUTTONSIZE = 118
BUTTONGAPSIZE = 10
BUTTONOFFSET = (118 - 76) / 2

REVEALSPEED = 8

XMARGIN = int((WINDOWWIDTH - 128 * 6))
YMARGIN = int((WINDOWHEIGHT - 128 * 5))

# Colours
WHITE           =(255, 255, 255)
BLACK           =(  0,   0,   0)
GREEN           =(  0, 200,   0)
RED             =(255,   0,   0)

# comeOnVer = ''
# comeOnUnits = ('u1', 'u2')

class team():
    def __init__(self, name, score, turns):
        self.name = name
        self.score = score
        self.turns = turns



def main(bookVersion, unitsList):
    comeOnVer = bookVersion
    comeOnUnits = unitsList
    global DISPLAYSURF, creeperSound, explosionImgs, FPSCLOCK
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    pygame.display.set_caption('The Creeper Game')

    gameBoard = generateRandomCreeperLocations()
    revealedBoxes = generateRevealedBoxesData(False)
    mousex = 0
    mousey = 0
    mouseClicked = False

    coverImages = fetchImages(comeOnVer, comeOnUnits)

    backgroundPath = os.path.join(baseImagePath, 'background.png')
    backgroundImage = pygame.image.load(backgroundPath)

    pngSequenceLoc = os.path.join(baseImagePath, 'explosionSeq')
    explosionSeq = [(os.path.join(pngSequenceLoc, pngFile)) for pngFile in os.listdir(pngSequenceLoc) if os.path.splitext(pngFile)[1] == '.png']
    explosionImgs = [pygame.image.load(image) for image in explosionSeq]


    creeperSoundPath = os.path.join(baseImagePath, 'creeperExplode.ogg')
    safeSoundPath = os.path.join(baseImagePath, 'blockClick.ogg')
    winSoundPath = os.path.join(baseImagePath, 'winSound.ogg')

    creeperSound = pygame.mixer.Sound(creeperSoundPath)
    safeSound = pygame.mixer.Sound(safeSoundPath)
    winSound = pygame.mixer.Sound(winSoundPath)



    teamOrder = generateTeamOrder()
    teamTurn = 0
    winner = None
    revealedCount = 0
    roundCount = 0
    creepersRemaining = 4

    


    # Main game loop
    while True:
        mouseClicked = False

        DISPLAYSURF.blit(backgroundImage, (0,0))
        
        drawScoreHouse(teamOrder)
        
        if teamTurn > 1:
            teamTurn = 0
        
        activeTeam = teamOrder[teamTurn]
        drawCreepersRemaining(creepersRemaining)
        
        # if gameState == 'PLAY':
        drawBoard(gameBoard, coverImages, revealedBoxes, activeTeam.name)      
        for event in pygame.event.get(): # Event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
                
                if mouseClicked == True:
                    revealedBoxes[boxx][boxy] = True
                    revealedCount += 1
                
                    #This part operates the team scoring
                    if gameBoard[boxx][boxy] == 'O': # If you find stone...
                        activeTeam.score += 1
                        safeSound.play()

                        
                    elif gameBoard[boxx][boxy] == 'C': #If you find a creeper...
                        activeTeam.score = 0
                        creepersRemaining -= 1
                        pygame.display.update()
                        explosionAnimation(activeTeam.name)
                    teamTurn += 1
                    activeTeam.turns += 1
                    
        pygame.display.update()

        winState, winner = checkWin(teamOrder, creepersRemaining, revealedCount)

        if winState:
            winSound.play()
            pygame.display.update()
            return winner, teamOrder

        

        # if turnsTaken['teamA'] == turnsTaken['teamB']: # The teams must take the same number of turns


        #     if revealedCount < 16: #Checks to see if someone has a winning score
                
                    
        #             if scores['teamA'] == 4 and scores['teamB'] == 4:
        #                 winner = 'both'
        #                 winSound.play()
        #                 pygame.display.update()
        #                 return winner, scores
                    
        #             elif scores['teamA'] == 4 and scores['teamB'] != 4:
        #                 winner = 'teamA'
        #                 winSound.play()
        #                 pygame.display.update()
        #                 return winner, scores

        #             elif scores['teamB'] == 4 and scores['teamA'] != 4:
        #                 winner = 'teamB'
        #                 winSound.play()
        #                 pygame.display.update()
        #                 return winner, scores


        #     elif revealedCount == 16: # If the board is fully revealed...
        #         winSound.play()
        #         if scores['teamA'] > scores['teamB']:
        #             winner = 'teamA'
        #         elif scores['teamB'] > scores['teamA']:
        #             winner = 'teamB'
        #         pygame.display.update()
        #         return winner, scores

            
        

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def checkWin(teamList, creepers, revealed):
    firstTeam = teamList[0]
    secondTeam = teamList[1]
    win = False
    winner = None
    if revealed == 16 or creepers == 0:
        win = True
        if firstTeam.score == secondTeam.score:
            winner = 'both'
        elif secondTeam.score > firstTeam.score:
            winner = secondTeam.name
        else:
            winner = firstTeam.name
    else:
        if firstTeam.score ==4 and secondTeam.score == 4:
            win = True
            winner = 'both'

        elif firstTeam.score == 4 and secondTeam.score < 3:
            win = True
            winner = firstTeam.name
        elif secondTeam.score == 4:
            win = True
            winner = secondTeam.name
    
    return win, winner
             
def leftTopCoordsOfBox (boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BUTTONSIZE + BUTTONGAPSIZE) + XMARGIN
    top = boxy * (BUTTONSIZE + BUTTONGAPSIZE) + YMARGIN
    return (left, top)

def centreCoordsOfBox(boxx, boxy):
    left = boxx * (BUTTONSIZE + BUTTONGAPSIZE) + (BUTTONSIZE/2) + XMARGIN
    top = boxy * (BUTTONSIZE + BUTTONGAPSIZE) +  (BUTTONSIZE/2) + YMARGIN
    return (left, top)

def fetchImages(bookVersion, comeOnUnits):
    comeOnVer = bookVersion
    firstUnitPath = os.path.join(workingDir, comeOnVer, comeOnUnits[0])
    secondUnitPath = os.path.join(workingDir, comeOnVer, comeOnUnits[1])
    
    firstUnitImages = [os.path.join(firstUnitPath, item) for item in os.listdir(firstUnitPath) if os.path.splitext(item)[1] == '.png']
    secondUnitImages = [os.path.join(secondUnitPath, item) for item in os.listdir(secondUnitPath) if os.path.splitext(item)[1] == '.png']

    random.shuffle(firstUnitImages)
    random.shuffle(secondUnitImages)

    if len(firstUnitImages) > 8 and len(secondUnitImages) > 8:
        selectedImagePaths = firstUnitImages[:8] + secondUnitImages[:8]
    elif len(firstUnitImages) < 8:
        offset = 16 - len(firstUnitImages)
        selectedImagePaths = firstUnitImages + secondUnitImages[:offset]
    elif len(secondUnitImages) < 8:
        offset = 16 - len(secondUnitImages)
        selectedImagePaths = firstUnitImages[:offset] + secondUnitImages


    pygameImages = []
    for path in selectedImagePaths:
        pygameImages.append(pygame.image.load(path))
    random.shuffle(pygameImages)


    rowA = pygameImages[0:4]
    rowB = pygameImages[4:8]
    rowC = pygameImages[8:12]
    rowD = pygameImages[12:16]

    return [rowA, rowB, rowC, rowD]

    return selectedImages

def drawBoard(currentBoard, coverBoard, revealedBoard, currentTeam):
    safeImg = pygame.image.load(os.path.join(baseImagePath, 'cobbleStone.png'))
    creeperImg = pygame.image.load(os.path.join(baseImagePath, 'creeperHead.png'))

    teamATurnImg = pygame.image.load(os.path.join(baseImagePath, 'teamATurnIndicator.png'))
    teamBTurnImg = pygame.image.load(os.path.join(baseImagePath, 'teamBTurnIndicator.png'))
    
    
    for boxx in range(len(currentBoard)):
        for boxy in range(len(currentBoard[boxx])):
            left, top = leftTopCoordsOfBox(boxx, boxy)

            if revealedBoard[boxx][boxy] == True:
                if currentBoard[boxx][boxy] == 'O':
                    DISPLAYSURF.blit(safeImg, (left, top))
                elif currentBoard[boxx][boxy] == 'C':
                    DISPLAYSURF.blit(creeperImg, (left, top))
            else:
                
                DISPLAYSURF.blit(coverBoard[boxx][boxy], ((left + BUTTONGAPSIZE/4), (top + BUTTONOFFSET)))
    if currentTeam == 'teamA':
        currentTeamImg = teamATurnImg
        DISPLAYSURF.blit(currentTeamImg, (0, 660))
    elif currentTeam == 'teamB':
        currentTeamImg = teamBTurnImg
        DISPLAYSURF.blit(currentTeamImg, (WINDOWWIDTH-256, 660))

def drawCreepersRemaining(creepers):
    creeperFont = pygame.font.SysFont('system', 70)
    creeperTextSurf = creeperFont.render(str(creepers), 1, WHITE)
    creeperTextRect = creeperTextSurf.get_rect()
    creeperTextRect.topleft = ((WINDOWWIDTH/2 + 10), 670)

    creeperIcon = pygame.image.load(os.path.join(baseImagePath, 'CreepersRemainingIcon.png'))
    creeperRect = creeperIcon.get_rect()
    creeperRect.topleft = ((WINDOWWIDTH/2 -90), 650)

    DISPLAYSURF.blit(creeperTextSurf, creeperTextRect)
    DISPLAYSURF.blit(creeperIcon, creeperRect)

def selectVersionScreen():
    menuBoard = ['CO1', 'CO2', 'CO3', 'CO4']
    menuY = 1

    CO1Menu = pygame.image.load(os.path.join(baseImagePath, 'CO1Button.png'))
    CO2Menu = pygame.image.load(os.path.join(baseImagePath, 'CO2Button.png'))
    CO3Menu = pygame.image.load(os.path.join(baseImagePath, 'CO3Button.png'))
    CO4Menu = pygame.image.load(os.path.join(baseImagePath, 'CO4Button.png'))

    menuList = [CO1Menu, CO2Menu, CO3Menu, CO4Menu]
    mousex, mousey = 0, 0
    while True:
        checkForQuit()
        DISPLAYSURF.blit(backgroundImage, (0,0))
        for menuX in range(0, len(menuBoard)):
            menuIcon = menuList[menuX]
            left, top = leftTopCoordsOfBox(menuX, menuY)
            DISPLAYSURF.blit(menuIcon, (left, top))
        mouseClicked = False
        for event in pygame.event.get(): # Event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if menuBoard[boxx] and boxy == menuY:
                drawHighlightBox(boxx, boxy)

                if mouseClicked == True:
                    return menuBoard[boxx]
            
                        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def selectUnitScreen(choice=None):
    menuBoard = [['u1', 'u2', 'u3', 'u4'], ['u5', 'u6', 'u7', 'u8']]
    UNITFONT = pygame.font.Font('freesansbold.ttf', 40)
    mousex, mousey = 0, 0
    selection = [0, 0]

    while True:
        checkForQuit()
        DISPLAYSURF.blit(backgroundImage, (0,0))
        for menuY in range(0, len(menuBoard)):
            for menuX in range(0, len(menuBoard[menuY])):
                unitText = menuBoard[menuY][menuX]
                wordSurf = UNITFONT.render(unitText, 1, WHITE)
                wordRect = wordSurf.get_rect()
                
                left, top = centreCoordsOfBox(menuX, menuY)
                wordRect.center = (left, top)

                DISPLAYSURF.blit(wordSurf, wordRect)

        mouseClicked = False
        for event in pygame.event.get(): # Event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:

            if boxy <= 1:
                # The mouse is currently over a box.
                if menuBoard[boxy] and menuBoard[boxy][boxx]:
                    drawHighlightBox(boxx, boxy)

                    if mouseClicked == True:
                        if boxy <=1:
                            selection[0] = boxx
                            selection[1] = boxy

                            return menuBoard[boxy][boxx], selection

        if choice:
            drawSelectionBox(choice[0], choice[1])

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
def drawGameOverScreen(winner, teams):
    drawScoreHouse(teams)

    winnerImagePath = None
    
    if winner == 'teamA':
        winnerImagePath = os.path.join(baseImagePath, 'winTileA.png')

    elif winner == 'teamB':
        winnerImagePath = os.path.join(baseImagePath, 'winTileB.png')
    
    else: 
        winnerImagePath = os.path.join(baseImagePath, 'winTileAll.png')

    winnerImage = pygame.image.load(winnerImagePath)

    while True:    
        checkForQuit()
        DISPLAYSURF.blit(winnerImage, ((128*2), (128)))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def explosionAnimation(team):
    if team == 'teamA':
        location = (36, 415)
    elif team == 'teamB':
        location = (805, 415)
    
    creeperSound.play()
    pygame.time.wait(1000)
    
    for step in range(0, len(explosionImgs), 2 ):
        checkForQuit()
        DISPLAYSURF.blit(explosionImgs[step], (location))
        pygame.display.update()
        FPSCLOCK.tick(FPS/2)

def getBoxAtPixel(x, y):
    for boxx in range(4):
        for boxy in range(4):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BUTTONSIZE, BUTTONSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawHighlightBox(boxx, boxy):
    hiColour = WHITE
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, hiColour, (left - 5, top - 5, BUTTONSIZE + 10, BUTTONSIZE + 10), 4)

def drawSelectionBox(boxx, boxy):
    hiColour = RED
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, hiColour, (left - 5, top - 5, BUTTONSIZE + 10, BUTTONSIZE + 10), 4)

def drawScoreHouse(teamList):

    firstTeam = teamList[0]
    secondTeam = teamList[1]

    if firstTeam.name == 'teamA':
        teamAScore = firstTeam.score
        teamBScore = secondTeam.score
    else:
        teamBScore = firstTeam.score
        teamAScore = secondTeam.score

    teamAHouseStateNumber = str(teamAScore).zfill(3)
    teamAHouseStateFileName = f'houseState_{teamAHouseStateNumber}.png'
    teamAHouseImagePath = os.path.join(baseImagePath, teamAHouseStateFileName)
    

    teamAHouseCoords = (0, 128*2)

    teamBHouseStateNumber = str(teamBScore).zfill(3)
    teamBHouseStateFileName = f'houseState_{teamBHouseStateNumber}.png'
    teamBHouseImagePath = os.path.join(baseImagePath, teamBHouseStateFileName)


    loadTeamAImage = pygame.image.load(teamAHouseImagePath)
    loadTeamBImage = pygame.image.load(teamBHouseImagePath)
    

    teamBHouseCoords = (128*6, 128*2)
    DISPLAYSURF.blit(loadTeamAImage, (teamAHouseCoords))
    DISPLAYSURF.blit(loadTeamBImage, (teamBHouseCoords))

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(4):
        revealedBoxes.append([val] * 4)
    return revealedBoxes

def generateTeamOrder():
    teams = [team('teamA', 0, 0), team('teamB', 0, 0)]
    random.shuffle(teams)
    return teams

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def game():
    #Initialization settings
    global DISPLAYSURF, creeperSound, explosionImgs, FPSCLOCK
    global backgroundImage, explosionImgs, creeperSound, safeSound, winSound

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    pygame.display.set_caption('The Creeper Game')
    mousex = 0
    mousey = 0

    # coverImages = fetchImages(comeOnVer, comeOnUnits)

    backgroundPath = os.path.join(baseImagePath, 'background.png')
    backgroundImage = pygame.image.load(backgroundPath)

    pngSequenceLoc = os.path.join(baseImagePath, 'explosionSeq')
    explosionSeq = [(os.path.join(pngSequenceLoc, pngFile)) for pngFile in os.listdir(pngSequenceLoc) if os.path.splitext(pngFile)[1] == '.png']
    explosionImgs = [pygame.image.load(image) for image in explosionSeq]


    creeperSoundPath = os.path.join(baseImagePath, 'creeperExplode.ogg')
    safeSoundPath = os.path.join(baseImagePath, 'blockClick.ogg')
    winSoundPath = os.path.join(baseImagePath, 'winSound.ogg')

    creeperSound = pygame.mixer.Sound(creeperSoundPath)
    safeSound = pygame.mixer.Sound(safeSoundPath)
    winSound = pygame.mixer.Sound(winSoundPath)

    
    while True:
        comeOnVer = selectVersionScreen()

        firstSelectedUnit, firtSelectionChoice = selectUnitScreen()
        secondSelectedUnit, secondSelectedChoice = selectUnitScreen(firtSelectionChoice)

        comeOnUnits = (firstSelectedUnit, secondSelectedUnit)

        while True:
            gameWinner, scores = main(comeOnVer, comeOnUnits)            
            drawGameOverScreen(gameWinner, scores)

if __name__ == "__main__":
    
    game()

    # print(fetchImages(comeOnVer, comeOnUnits))
    # print(drawBackground())