import os
import json
import fnmatch
from tkinter.messagebox import showinfo
from unicodedata import name
from classes.Ship import Ship
from classes.Mod import Mod
from classes.localLoadedJSON import localLoadedJSON
from processModJSONFiles import rollup_mods

def throwError(errorText):
    showinfo('Failure', 'An error occurred - ' + errorText[0])

def resolveShipType(shipType):
    match shipType:
        case 'derelict':
            return 'RandomDerelict'
        case 'police':
            return 'RandomPoliceShip'
        case 'scav':
            return 'RandomScavShip'
        case 'random':
            return 'RandomShip'
        case _:
            print('¯\_(ツ)_/¯')
            return

def loadModData():
    loadOrderArr: list = localLoadedJSON('../../loading_order.json').data[0]['aLoadOrder']
    mods: list[Mod] = []

    for dirName, subdirList, fileList in os.walk('../../'):
        for fileName in fileList:
            if fileName == 'mod_info.json':
                modJSON: dict[str, str] = localLoadedJSON(dirName + '\mod_info.json').data[0]
                if modJSON['strName'] == 'tt-mod-manager': continue
                pathName = dirName[6:]
                mods.append(Mod(modJSON['strName'], pathName, modJSON['strAuthor'], modJSON['strName'] in loadOrderArr, [], False))

    # compute files touched by mods
    touchedFiles = getTouchedJSONsFromMods()
    for mod in mods:
        mod.files_touched = touchedFiles[mod.pathName]
        
    return mods

def loadShipData(shipType):
    shipType = resolveShipType(shipType)
    if not shipType:
        return
    ships = []

    for dirName, subdirList, fileList in os.walk('../../'):
        if '\data\ships' in dirName:
            for fileName in fileList:
                if '.json' in fileName:
                    ships.append(Ship(
                        dirName[6:-11], fileName[0:-5], 0, 0))

    with open('../../../StreamingAssets/data/loot/loot.json') as fp:
        data = json.load(fp)

        for item in data:
            # Following code is derpy as hell :( - Will fix later
            if item['strName'] == shipType:
                baseGameShipsRAW = item['aCOs'][0].split("|")
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

    return ships + baseGameShipsObject


def saveShipChanges(lst, shipType):
    try:
        shipType = resolveShipType(shipType)
        if not shipType:
            return

        # remove not-included ships
        lst = list(filter(lambda x: x.__getattr__('included').get() == 1, lst))

        # check lst is not empty
        if len(lst) > 0:
            # validate weights are numeric values
            for ship in lst:
                try:
                    ship.__getattr__('weight').get()
                except:
                    raise ValueError('Ship weights must be numeric values')

            # convert values to percentages of 1.0
            total = 0
            for ship in lst:
                total += float(ship.__getattr__('weight').get())

            for ship in lst:
                ship.__setattr__('weight', round(
                    float(ship.__getattr__('weight').get()) / total, 5))

            # make last value large to avoid floating point error
            lst[-1].__setattr__('weight', 0.5)

            # create output string
            shipJsonString = ''
            for ship in lst:
                shipValueString = ship.__getattr__(
                    'name') + '=' + str(ship.__getattr__('weight')) + 'x1|'
                shipJsonString += shipValueString
            shipJsonString = shipJsonString[0:-1]
        else:
            raise ValueError('Selected ships must be more than one')

        # open loot file, grab data and replace with new ship data  
        with open('../data/loot/loot.json') as fp:
            data = json.load(fp)
            for item in data:
                if item['strName'] == shipType:
                    item['aCOs'] = shipJsonString
            fp.close()

        # open loot file in overwrite mode, dump in new json
        with open('../data/loot/loot.json', 'w') as fp:
            json.dump(data, fp)
            fp.close()

        showinfo('Success', shipType.capitalize() + ' ships saved')

        # extract mods enabled
        enabledModsList = list(filter(lambda x: x.__getattr__('mod') != 'BaseGame', lst))
        
        # update loading_order.json
        checkLoadOrder(enabledModsList)

        showinfo('Success', 'loading_order.json updated')
    except ValueError as error:
        throwError(error.args)

def checkLoadOrder(enabledModsList: list[str]):
    with open('../../loading_order.json') as fp:
        data = json.load(fp)
        for item in data:
                if item['strName'] == 'Mod Loading Order':
                    loadOrder: list[str] = ["core"]
                    # remove tt-mod-loader if present
                    # for entry in loadOrder:
                    #     if entry == 'tt-mod-manager':
                    #         loadOrder.remove('tt-mod-manager')

                    # add any new mods not in the mod load order
                    for mod in enabledModsList:
                        if mod not in loadOrder: loadOrder.append(mod)

                    # put the mod manager on the end
                    loadOrder.append('tt-mod-manager')

                    # replace list in data
                    print(loadOrder)
                    item['aLoadOrder'] = loadOrder

    with open('../../loading_order.json', 'w') as fp:
        json.dump(data, fp)
        fp.close()

def getTouchedJSONsFromMods():
    mods = {}
    for dirName, subdirList, fileList in os.walk('../../'):
        jsonFiles = fnmatch.filter(fileList, '*.json')
        dirName = dirName.replace('\\', '/')
        if len(jsonFiles) > 0:
            modName = dirName.split('/')[2]
            if modName == '': continue 
            modifiedDir = '/' + dirName[(7+len(modName)):len(dirName)]
            if '/data/ships' in modifiedDir: continue
            if modName not in mods:
                mods[modName] = {}
            mods[modName][modifiedDir] = jsonFiles
    return mods

def saveModChanges(mods: list[Mod]):
    try:
        # combine all mod jsons
        rollup_mods(mods)

        showinfo('Success', 'Mod JSONs merged')

        # update loading_order.json
        enabledModsList = []
        for mod in mods:
            if mod.included.get():
                enabledModsList.append(mod.name)
        checkLoadOrder(enabledModsList)

        showinfo('Success', 'loading_order.json updated')
    except ValueError as error:
        throwError(error.args)