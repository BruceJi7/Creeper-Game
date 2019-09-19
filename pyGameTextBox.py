import pygame, sys
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
#colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)




def main():
    pygame.init()

    global DISPLAYSURF, BASICFONT

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    pygame.display.set_caption('Text Box Test')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 14)

    while True:
        drawTextBox(200, 100, 10, 10, (255, 255, 255))
        pygame.display.update()
        checkForQuit()


def drawTextBox(width, height, xpos, ypos, color):

    textRect = pygame.draw.rect(DISPLAYSURF, color, (xpos, ypos, width, height))
    text = ''
    wordSurf = BASICFONT.render(text, 1, BLACK)
    wordRect = wordSurf.get_rect()
    wordRect.topleft = (xpos+5, ypos+5)

    active = False
    completed = False
    while completed == False:
        checkForQuit()
        DISPLAYSURF.blit(wordSurf, wordRect)
        
        for event in pygame.event.get():

            if active == False:
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if textRect.collidepoint(mousex, mousey):
                        active = True


            elif active == True:
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if not textRect.collidepoint(mousex, mousey):
                        active = False

        
                if pygame.key.get_focused():
                    key = event.key
                    print(pygame.key.name(key))      
        pygame.display.update()
        



        

    




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

if __name__ == "__main__":
    main()