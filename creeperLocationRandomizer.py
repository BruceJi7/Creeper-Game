import random, pprint

def generateRandomCreeperLocations():
    safeCells = ['O' for n in range(0,12)]
    creeperCells = ['C' for n in range(0,4)]
    allCells = safeCells + creeperCells

    randomisedLocations = allCells.copy()
    random.shuffle(randomisedLocations)


    rowA = randomisedLocations[0:4]
    rowB = randomisedLocations[4:8]
    rowC = randomisedLocations[8:12]
    rowD = randomisedLocations[12:16]

    return [rowA, rowB, rowC, rowD]

if __name__ == "__main__":
    pprint.pprint(generateRandomCreeperLocations())
