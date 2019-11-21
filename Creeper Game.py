from creeperLocationRandomizer import generateRandomCreeperLocations
import creeperCommonImages

import random, sys, time, pygame, os
from pygame.locals import *
import pygame.freetype

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
    def __init__(self, name, score, turns, overallScore, foundCreeper, creepersFound):
        self.name = name
        self.score = score
        self.turns = turns
        self.overallScore = overallScore
        self.foundCreeper = foundCreeper
        self.creepersFound = creepersFound


class Menubutton():
    def __init__(self, path, series, gameType, state='up', surface=None):
        self.path = path
        self.__state = state
        self.series = series
        self.gameType = gameType
        self.__surface = surface
        self.rect = self.makeRect()
        
        # self.surface = self.path[self.state]
        # self.rect = self.surface.get_rect()




    @property
    def state(self):
        return self.__state


    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def surface(self):
        return self.path[self.state]

    # def makeSurf(self):
    #     return self.path[self.state]

    def makeRect(self):
        return self.surface.get_rect()

    # def surface(self):
    #     return self.path[self.state]

    # def rect(self):
    #     return self.path.get_rect()


def main(bookVersion, unitsList, teamList):
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

    coverImages = creeperCommonImages.fetchImages(comeOnVer, comeOnUnits[0], comeOnUnits[1])

    backgroundImage = creeperCommonImages.backgroundImage
    explosionImgs = creeperCommonImages.explosionSeq


    creeperSoundPath = os.path.join(baseImagePath, 'creeperExplode.ogg')
    safeSoundPath = os.path.join(baseImagePath, 'blockClick.ogg')
    winSoundPath = os.path.join(baseImagePath, 'winSound.ogg')

    creeperSound = pygame.mixer.Sound(creeperSoundPath)
    safeSound = pygame.mixer.Sound(safeSoundPath)
    winSound = pygame.mixer.Sound(winSoundPath)



    teamOrder = generateTeamOrder(teamList)
    for team in teamOrder:
        team.score = 0
        team.creepersFound = 0
    
    teamTurn = 0
    winner = None
    revealedCount = 0
    roundCount = 0
    creepersRemaining = 4
    blocksRemaining = 12

    


    # Main game loop
    while True:
        mouseClicked = False

        DISPLAYSURF.blit(backgroundImage, (0,0))
        
        drawScoreHouse(teamOrder)
        drawRoundsWon(teamOrder)
        
        if teamTurn > 1:
            teamTurn = 0
        
        activeTeam = teamOrder[teamTurn]
        drawCreepersRemaining(creepersRemaining, blocksRemaining)
        drawCreeperDamage(teamOrder)
        
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
                        blocksRemaining -= 1
                        activeTeam.foundCreeper=False

                        
                    elif gameBoard[boxx][boxy] == 'C': #If you find a creeper...
                        activeTeam.score = 0
                        activeTeam.creepersFound += 1
                        creepersRemaining -= 1
                        if activeTeam.foundCreeper:
                            activeTeam.overallScore -= 1
                               
                        else:
                            activeTeam.foundCreeper = True
                        pygame.display.update()
                        explosionAnimation(activeTeam.name)
                    teamTurn += 1
                    activeTeam.turns += 1
        
        
        pygame.display.update()

        winState, winner = checkWin(teamOrder, creepersRemaining, revealedCount)

        if winState:
            winSound.play()
            pygame.display.update()
            drawCreepersRemaining(creepersRemaining, blocksRemaining)
            
            return winner, teamOrder

        


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
            firstTeam.overallScore += 1
            secondTeam.overallScore += 1
        elif secondTeam.score > firstTeam.score:
            winner = secondTeam.name
            secondTeam.overallScore += 1

        else:
            winner = firstTeam.name
            firstTeam.overallScore += 1
    else:
        if firstTeam.score ==4 and secondTeam.score == 4:
            win = True
            winner = 'both'
            firstTeam.overallScore += 1
            secondTeam.overallScore += 1
            

        elif firstTeam.score == 4 and secondTeam.score < 3:
            win = True
            winner = firstTeam.name
            firstTeam.overallScore += 1
        elif secondTeam.score == 4:
            win = True
            winner = secondTeam.name
            secondTeam.overallScore += 1
    
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

def drawBoard(currentBoard, coverBoard, revealedBoard, currentTeam):
    safeImg = creeperCommonImages.blockTiles['cobble']
    creeperImg = creeperCommonImages.blockTiles['creeper']

    teamATurnImg = creeperCommonImages.teamTurnIndicator['teamA']
    teamBTurnImg = creeperCommonImages.teamTurnIndicator['teamB']
    
    
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
        DISPLAYSURF.blit(currentTeamImg, (0, 180))
    elif currentTeam == 'teamB':
        currentTeamImg = teamBTurnImg
        DISPLAYSURF.blit(currentTeamImg, (WINDOWWIDTH-256, 180))

def drawCreepersRemaining(creepers, blocks):

    creeperIconLoc = 266
    blockIconLoc = WINDOWWIDTH - creeperIconLoc - 80

    creeperFont = pygame.font.SysFont('minecraft', 70)

    percentFont = pygame.font.SysFont('minecraft', 45)

    creeperTextSurf = creeperFont.render(str(creepers), 1, WHITE)
    creeperTextRect = creeperTextSurf.get_rect()
    creeperTextRect.topleft = ((creeperIconLoc+80+10), 670)

    creeperIcon = creeperCommonImages.remainingIcons['creeper']
    creeperRect = creeperIcon.get_rect()
    creeperRect.topleft = (creeperIconLoc, 650)


    blockTextSurf = creeperFont.render(str(blocks), 1, WHITE)
    blockTextRect = blockTextSurf.get_rect()
    blockTextRect.topleft = ((blockIconLoc-75), 670)

    blockIcon = creeperCommonImages.remainingIcons['cobble']
    blockRect = blockIcon.get_rect()
    blockRect.topleft = (blockIconLoc, 650)

    prePercent = (creepers / blocks)
    prePercent = round(prePercent, 3)
    percent = int(prePercent * 100)

    percentTextSurf = percentFont.render(f'{str(percent)}%', 1, WHITE)
    percentTextRect = percentTextSurf.get_rect()
    percentTextRect.topleft = ((WINDOWWIDTH/2 -30) , 680)

    DISPLAYSURF.blit(creeperTextSurf, creeperTextRect)
    DISPLAYSURF.blit(creeperIcon, creeperRect)

    DISPLAYSURF.blit(blockTextSurf, blockTextRect)
    DISPLAYSURF.blit(blockIcon, blockRect)

    DISPLAYSURF.blit(percentTextSurf, percentTextRect)

def drawRoundsWon(teamList):
    firstTeam = teamList[0]
    secondTeam = teamList[1]

    if firstTeam.name == 'teamA':
        teamAScore = firstTeam.overallScore
        teamBScore = secondTeam.overallScore
    else:
        teamAScore = secondTeam.overallScore
        teamBScore = firstTeam.overallScore
    
    scoreFont = pygame.font.SysFont('minecraft', 40)

    teamAScoreSurf = scoreFont.render(str(teamAScore), 1, WHITE)
    teamAScoreRect = teamAScoreSurf.get_rect()
    teamAScoreRect.topleft = (215, 130)


    teamBScoreSurf = scoreFont.render(str(teamBScore), 1, WHITE)
    teamBScoreRect = teamBScoreSurf.get_rect()
    teamBScoreRect.topleft = (785, 130)

    DISPLAYSURF.blit(teamAScoreSurf, teamAScoreRect)
    DISPLAYSURF.blit(teamBScoreSurf, teamBScoreRect)
    
def drawCreeperDamage(teamList):

    firstTeam = teamList[0]
    secondTeam = teamList[1]

    if firstTeam.name == 'teamA':
        teamADamage = firstTeam.creepersFound
        teamBDamage = secondTeam.creepersFound
    else:
        teamBDamage = firstTeam.creepersFound
        teamADamage = secondTeam.creepersFound

    teamADamageImg = creeperCommonImages.houseBase[teamADamage]
    teamBDamageImg = creeperCommonImages.houseBase[teamBDamage]

    teamADamageCoords = (0, 640)
    teamBDamageCoords = (768, 640)

    DISPLAYSURF.blit(teamADamageImg, (teamADamageCoords))
    DISPLAYSURF.blit(teamBDamageImg, (teamBDamageCoords))

def selectSeries():

    COButton = creeperCommonImages.menuButtons['bookMenu']['bookMenuCO']
    CORect = COButton.get_rect()
    CORect.topleft = (XMARGIN, YMARGIN)

    EBButton = creeperCommonImages.menuButtons['bookMenu']['bookMenuEB']
    EBRect = EBButton.get_rect()
    EBRect.topleft = (XMARGIN+256, YMARGIN)


 

    while True:
        checkForQuit()
        DISPLAYSURF.blit(backgroundImage, (0,0))
        DISPLAYSURF.blit(COButton, CORect)
        DISPLAYSURF.blit(EBButton, EBRect)
        
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseClicked = True
        
        if mouseClicked == True:
            if CORect.collidepoint(mouseX, mouseY):
                return 'ComeOn'

            elif EBRect.collidepoint(mouseX, mouseY):
                return 'EngBus'

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def selectVersionScreen(whatbook):
    if whatbook == 'ComeOn':

        menuBoard = ['CO1', 'CO2', 'CO3', 'CO4']
        menuY = 1

        CO1Menu = creeperCommonImages.menuButtons['COMenu']['CO1Button']
        CO2Menu = creeperCommonImages.menuButtons['COMenu']['CO2Button']
        CO3Menu = creeperCommonImages.menuButtons['COMenu']['CO3Button']
        CO4Menu = creeperCommonImages.menuButtons['COMenu']['CO4Button']

        menuList = [CO1Menu, CO2Menu, CO3Menu, CO4Menu]
    elif whatbook == 'EngBus':
        menuBoard = ['EB2', 'EB3', 'EB4']
        menuY = 1

        EB2Menu = creeperCommonImages.menuButtons['EBMenu']['EB2Button']
        EB3Menu = creeperCommonImages.menuButtons['EBMenu']['EB3Button']
        EB4Menu = creeperCommonImages.menuButtons['EBMenu']['EB4Button']

        menuList = [EB2Menu, EB3Menu, EB4Menu]
    
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
            try:
                if menuBoard[boxx] and boxy == menuY:
                    drawHighlightBox(boxx, boxy)

                if mouseClicked == True:
                    return menuBoard[boxx]
            except:
                continue
                        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def selectUnitScreen():
    firstUnitBoard = [['1', '2', '3', '4'], ['5', '6', '7', '8']]
    secondUnitBoard = [['1', '2', '3', '4'], ['5', '6', '7', '8']]
    UNITFONT = pygame.font.SysFont('Minecraft', 40)
    mousex, mousey = 0, 0
    selection = [0, 0]
    choices = [None, None]
    firstUnitChoice = None
    secondUnitChoice = None

    buttonImg = creeperCommonImages.buttonState['up']
    buttonHoverImg = creeperCommonImages.buttonState['hover']
    buttonDownImg = creeperCommonImages.buttonState['down']

    frameImg = creeperCommonImages.frameImg

    buttonState = buttonImg

    buttonRect = buttonState.get_rect()
    buttonRect.topleft = (384, 650)

    while True:
        checkForQuit()
        DISPLAYSURF.blit(backgroundImage, (0,0))

        
        DISPLAYSURF.blit(buttonState, buttonRect)


        for Y in range(0, 4):
            for X in range (0, 4):
                frameRect = frameImg.get_rect()
                left, top = centreCoordsOfBox(X, Y)
                frameRect.center = (left, top)
                DISPLAYSURF.blit(frameImg, frameRect)


        
        for menuY in range(0, 2):
            for menuX in range(0, 4):
                unitText = firstUnitBoard[menuY][menuX]
                wordSurf = UNITFONT.render(unitText, 1, WHITE)
                wordRect = wordSurf.get_rect()
                
                
                left, top = centreCoordsOfBox(menuX, menuY)
                wordRect.center = (left, top)
                
                DISPLAYSURF.blit(wordSurf, wordRect)
                

        
        for menuY in range(0, 2):
            for menuX in range(0, 4):
                unitText = secondUnitBoard[menuY][menuX]
                wordSurf = UNITFONT.render(unitText, 1, WHITE)
                wordRect = wordSurf.get_rect()

                
                
                left, top = centreCoordsOfBox(menuX, menuY+2)
                wordRect.center = (left, top)

                DISPLAYSURF.blit(wordSurf, wordRect)

        

        mouseClicked = False
        buttonDown = False
        for event in pygame.event.get(): # Event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        try:
            boxx, boxy = getBoxAtPixel(mousex, mousey)
        except:
            continue

         

        if boxx != None and boxy != None:

            if boxy in (0, 1) :
                # The mouse is currently over a box.
                if firstUnitBoard[boxy] and firstUnitBoard[boxy][boxx]:
                    drawHighlightBox(boxx, boxy)

                    if mouseClicked == True:
                        if boxy in (0, 1):
   
                            firstUnitChoice = firstUnitBoard[boxy][boxx]

                            choices[0] = [boxx, boxy]

            if boxy in (2, 3):
                if secondUnitBoard[boxy-2] and secondUnitBoard[boxy-2][boxx]:
                    drawHighlightBox(boxx, boxy)

                    if mouseClicked == True:
                        if boxy in (2, 3):
                            secondUnitChoice = secondUnitBoard[boxy-2][boxx]

                            choices[1] = [boxx, boxy]               

        if choices[0]:
            drawSelectionBox(choices[0][0], choices[0][1])
        if choices[1]:
            drawSelectionBox(choices[1][0], choices[1][1])

        if buttonRect.collidepoint(mousex, mousey):
            if mouseClicked == False:
                buttonState = buttonHoverImg

            elif mouseClicked == True:
                buttonState = buttonDownImg
                if firstUnitChoice and secondUnitChoice:
                    return (f'u{firstUnitChoice}', f'u{secondUnitChoice}')
            
        else:
            buttonState = buttonImg



        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
def mainMenu():

    COButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['comeOnBook'], 'ComeOn', 'normal')
    COButton.rect.center = ((128*3), (128*2))

    
    EBButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['engBusBook'], 'EngBus', 'normal')
    EBButton.rect.center = ((128*5), (128*2))

    CORandomButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['comeOnRandom'], 'ComeOn', 'unitSelect')
    CORandomButton.rect.center = ((128*2.5), (128*3.5))

    EBRandomButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['engBusRandom'], 'EngBus', 'unitSelect')
    EBRandomButton.rect.center = ((128*5.5), (128*3.5))

    CORainbowButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['comeOnRainbow'], 'ComeOn', 'random')
    CORainbowButton.rect.center = ((128*2.5), (128*4.5))

    EBRainbowButton = Menubutton(creeperCommonImages.menuButtons['mainMenu']['engBusRainbow'], 'EngBus', 'random')
    EBRainbowButton.rect.center = ((128*5.5), (128*4.5))

    result = None
    mouseClicked = None

    while True:
        checkForQuit()
        DISPLAYSURF.blit(backgroundImage, (0,0))

        


        mouseX, mouseY = pygame.mouse.get_pos()
        
        
        for event in pygame.event.get(): # Event handling loop
            if event.type == MOUSEBUTTONUP:
                mouseClicked = True


        buttons = [COButton, EBButton, CORandomButton, EBRandomButton, CORainbowButton, EBRainbowButton]

        for button in buttons:
            if button.rect.collidepoint(mouseX, mouseY):
                button.state = 'hover'
                if mouseClicked:
                    return (button.series, button.gameType)

            else:
                button.state = 'up'
        
        # if mouseState == 0:
        #     if result:
        #         return result

        # if COButton.rect.collidepoint(mouseX, mouseY):
        #     COButton.state = 'hover'
        #     if mouseClicked:
        #         return 'normal', 'comeOn'
        # elif EBButton.rect.collidepoint(mouseX, mouseY):
        #     EBButton.state = 'hover'
        #     if mouseClicked:
        #         return 'normal', 'engBus'
        # elif CORandomButton.rect.collidepoint(mouseX, mouseY):
        #     CORandomButton.state = 'hover'
        # elif EBRandomButton.rect.collidepoint(mouseX, mouseY):
        #     EBRandomButton.state = 'hover'
        # elif CORainbowButton.rect.collidepoint(mouseX, mouseY):
        #     CORainbowButton.state = 'hover'
        # elif EBRainbowButton.rect.collidepoint(mouseX, mouseY):
        #     EBRainbowButton.state = 'hover'

        # else:
        #     COButton.state = 'up'
        #     EBButton.state = 'up'
        #     CORandomButton.state = 'up'
        #     EBRandomButton.state = 'up'
        #     CORainbowButton.state = 'up'
        #     EBRainbowButton.state = 'up'

        for event in pygame.event.get(): # Event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()

        
        DISPLAYSURF.blit(COButton.surface, COButton.rect)
        DISPLAYSURF.blit(EBButton.surface, EBButton.rect)
        DISPLAYSURF.blit(CORandomButton.surface, CORandomButton.rect)
        DISPLAYSURF.blit(EBRandomButton.surface, EBRandomButton.rect)
        DISPLAYSURF.blit(CORainbowButton.surface, CORainbowButton.rect)
        DISPLAYSURF.blit(EBRainbowButton.surface, EBRainbowButton.rect)



        pygame.display.update()
        FPSCLOCK.tick(FPS)
        



def drawGameOverScreen(winner, teams):
    DISPLAYSURF.blit(backgroundImage, (0,0))
    drawScoreHouse(teams)
    drawCreeperDamage(teams)
    drawRoundsWon(teams)

    winnerImage = creeperCommonImages.winner[winner]
    

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

    
    teamAHouseImage = creeperCommonImages.houseState[teamAScore]   
    teamAHouseCoords = (0, 128*2)

    teamBHouseImage = creeperCommonImages.houseState[teamBScore]
    teamBHouseCoords = (128*6, 128*2)


    DISPLAYSURF.blit(teamAHouseImage, (teamAHouseCoords))
    DISPLAYSURF.blit(teamBHouseImage, (teamBHouseCoords))

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(4):
        revealedBoxes.append([val] * 4)
    return revealedBoxes

def generateTeamOrder(teams):
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

    teamA = team('teamA', 0, 0, 0, False, 0)
    teamB = team('teamB', 0, 0, 0, False, 0)

    teams = [teamA, teamB]
    # coverImages = fetchImages(comeOnVer, comeOnUnits)

    backgroundImage = creeperCommonImages.backgroundImage   
    explosionImgs = creeperCommonImages.explosionSeq

    creeperSoundPath = os.path.join(baseImagePath, 'creeperExplode.ogg')
    safeSoundPath = os.path.join(baseImagePath, 'blockClick.ogg')
    winSoundPath = os.path.join(baseImagePath, 'winSound.ogg')

    creeperSound = pygame.mixer.Sound(creeperSoundPath)
    safeSound = pygame.mixer.Sound(safeSoundPath)
    winSound = pygame.mixer.Sound(winSoundPath)

    BGMPath = os.path.join(baseImagePath, 'creeperBMG.ogg')
    BMG = pygame.mixer.music.load(BGMPath)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    
    while True:
        book, gameType = mainMenu()
        if gameType == 'normal':
            bookVer = selectVersionScreen(book)
        else:
            continue

        firstSelectedUnit, secondSelectedUnit = selectUnitScreen()
        
        comeOnUnits = (firstSelectedUnit, secondSelectedUnit)

        while True:
            gameWinner, scores = main(bookVer, comeOnUnits, teams)            
            drawGameOverScreen(gameWinner, scores)

if __name__ == "__main__":
    
    game()