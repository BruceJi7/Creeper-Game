import pygame, os

pygame.init()

baseImagePath = r'C:\Come On Python Games\resources\creeperGame\commonImages'


backgroundImage = pygame.image.load(os.path.join(baseImagePath, 'background.png'))


menuButtonsPath = r'C:\Come On Python Games\resources\creeperGame\commonImages\menuButtons' 
menuButtons = {
    'BookMenu': 
                {
            'BookMenuCO' : pygame.image.load(os.path.join(menuButtonsPath, 'BookMenuCO.png')),
            'BookMenuEB' : pygame.image.load(os.path.join(menuButtonsPath, 'BookMenuEB.png'))
                },
    
    'COMenu': 
                {    
            'CO1Button'  : pygame.image.load(os.path.join(menuButtonsPath, 'CO1Button.png')),
            'CO2Button'  : pygame.image.load(os.path.join(menuButtonsPath, 'CO2Button.png')),
            'CO3Button'  : pygame.image.load(os.path.join(menuButtonsPath, 'CO3Button.png')),
            'CO4Button'  : pygame.image.load(os.path.join(menuButtonsPath, 'CO4Button.png'))
                },
    
    'EBMenu':
                {
            'EB2Button' : pygame.image.load(os.path.join(menuButtonsPath, 'EB2Button.png')),
            'EB3Button' : pygame.image.load(os.path.join(menuButtonsPath, 'EB3Button.png')),
            'EB4Button' : pygame.image.load(os.path.join(menuButtonsPath, 'EB4Button.png'))            
                },
    
}




houseBasePath = r'C:\Come On Python Games\resources\creeperGame\commonImages\houseBase'
houseBase = [
    pygame.image.load(os.path.join(houseBasePath, 'houseBase_000.png')),
    pygame.image.load(os.path.join(houseBasePath, 'houseBase_001.png')),
    pygame.image.load(os.path.join(houseBasePath, 'houseBase_002.png')),
    pygame.image.load(os.path.join(houseBasePath, 'houseBase_003.png')),
]



houseStatePath = r'C:\Come On Python Games\resources\creeperGame\commonImages\houseState' 
houseState = [
    pygame.image.load(os.path.join(houseStatePath, 'houseState_000.png')),
    pygame.image.load(os.path.join(houseStatePath, 'houseState_001.png')),
    pygame.image.load(os.path.join(houseStatePath, 'houseState_002.png')),
    pygame.image.load(os.path.join(houseStatePath, 'houseState_003.png')),
    pygame.image.load(os.path.join(houseStatePath, 'houseState_004.png')),
]



winnerPath = r'C:\Come On Python Games\resources\creeperGame\commonImages\winner'
winner = {
    'teamA' : pygame.image.load(os.path.join(winnerPath, 'winTileA.png')),
    'teamB' : pygame.image.load(os.path.join(winnerPath, 'winTileB.png')),
    'both'  : pygame.image.load(os.path.join(winnerPath, 'winTileAll.png'))
} 


explosionSeqPath = r'C:\Come On Python Games\resources\creeperGame\commonImages\explosionSeq'
explosionFiles = [(os.path.join(explosionSeqPath, pngFile)) for pngFile in os.listdir(explosionSeqPath) if os.path.splitext(pngFile)[1] == '.png']
explosionSeq = [pygame.image.load(image) for image in explosionFiles]



