import os
import json

class Ship:
    def __init__(self, mod, name, included, weight ):
        self.mod = mod
        self.name = name
        self.included = included
        self.weight = weight
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)

def loadShipData():
    ships = []

    for dirName, subdirList, fileList in os.walk('../../'):
        if '\data\ships' in dirName:
            for fileName in fileList:
                if '.json' in fileName:
                    ships.append(Ship(dirName[6:-11], fileName[0:-5], 0, 0))

    with open('../../../StreamingAssets/data/loot/loot.json') as fp:
        data = json.load(fp)

        for item in data:
            # Following code is derpy as hell :( - Will fix later
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
                        Ship('BaseGame', shipData[0], 1, shipData[1]))
        fp.close()

    test = ships + baseGameShipsObject
    return test


def saveChanges(lst):
    # convert values to percentages of 1.0
    total = 0
    for ship in lst:
        total += float(ship.__getattr__('weight').get())

    for ship in lst:
        ship.__setattr__('weight', round(float(ship.__getattr__('weight').get()) / total, 4))

    # make last value large to avoid floating point error
    lst[-1].__setattr__('weight', 0.5)

    # create output string
    shipJsonString = ''
    for ship in lst:
        if ship.__getattr__('included').get() == 1:
            shipValueString = ship.__getattr__('name') + '=' + str(ship.__getattr__('weight')) + 'x1,'
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
    