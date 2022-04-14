import os
import json

class ship:
    def __init__(self, name, weight, included, modded):
        self.name = name
        self.weight = weight
        self.included = included
        self.modded = modded

def loadShipData():
    ships = []
    # for fileName in os.listdir('../../StreamingAssets/data/ships'):
    #     if '.json' in fileName:
    #         ships.append({'baseGame': fileName[0:-5]})

    for dirName, subdirList, fileList in os.walk('../../'):
        if '\data\ships' in dirName:
            for fileName in fileList:
                if '.json' in fileName:
                    ships.append([dirName[9:-11], fileName[0:-5], 0, 0])

    with open('../../../StreamingAssets/data/loot/loot.json') as fp:
        data = json.load(fp)

        for item in data:
            if item.get('strName') == 'RandomDerelict':
                baseGameShipsRAW = item.get('aCOs')[0].split("|")
                length = len(baseGameShipsRAW)
                baseGameShipsObject = []
                count = 0
                total = 0
                for ship in baseGameShipsRAW:
                    count += 1
                    shipData = ship[0:-2].split('=')
                    if not count >= length:
                        total += float(shipData[1])
                    else:
                        shipData[1] = round((1 - total), 4)
                    baseGameShipsObject.append(
                        ['BaseGame', shipData[0], 1, shipData[1]])
        fp.close()

    return ships + baseGameShipsObject


def saveChanges(lst):
    # convert values to percentages of 1.0
    total = 0
    for ship in lst:
        total += float(ship[3].get())

    for ship in lst:
        ship[3] = round(float(ship[3].get()) / total, 4)

    # make last value large to avoid floating point error
    lst[-1][3] = 0.5

    # create output string
    shipJsonString = ''
    for ship in lst:
        if ship[2].get() == 1:
            shipValueString = ship[1] + '=' + str(ship[3]) + 'x1,'
            shipJsonString += shipValueString
    shipJsonString = shipJsonString[0:-1]

    with open('../data/loot/loot.json') as fp:
        data = json.load(fp)
        for item in data:
            if item.get('strName') == 'RandomDerelict':
                item['aCOs'] = shipJsonString
        fp.close()

    with open('../data/loot/loot.json', 'w') as fp:
        json.dump(data, fp)
        fp.close()
    