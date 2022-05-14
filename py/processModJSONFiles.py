import shutil
import useScriptCompareFunctions
import json
import os
from classes.Mod import Mod

def get_json(path):
  with open(path) as fp:
    jsonDump = json.load(fp)
    fp.close() # force file stream closed, not sure its necessary but ¯\_(ツ)_/¯
    return jsonDump

def merge_mod_info(modInfoPath):
  pass

def clean_working_dir():
  # this function serves to clear any existing files in mod manager that were previously incorporated
  for dirName in os.listdir('../data'):
    shutil.rmtree('../data/' + dirName)

def process_mod_file_structure(mod, modJSONPaths):
  modPathRoute = '../../'
  localPathRoute = '..'

  # create the mandatory ships dir
  if not os.path.exists('../data/ships'):
    os.makedirs('../data/ships')

  # process all json files
  for path in modJSONPaths:
    for file in modJSONPaths[path]:
      compiledLocalPath = localPathRoute + path + '/'
      compiledModPath = modPathRoute + mod + path + '/'
      if file == 'mod_info.json':
        merge_mod_info(compiledModPath + file)
        continue
      modJson = get_json(compiledModPath + file)
      if os.path.exists(compiledLocalPath + file):
        # print('it exists!')
        # print(compiledLocalPath + file)
        existingJSON = get_json(compiledLocalPath + file)
        mergedJSON = useScriptCompareFunctions.compareDicts(existingJSON, modJson, file)
        if mergedJSON['level'] != 3:
          with open(compiledLocalPath + file, 'w') as fp:
            json.dump(mergedJSON['json'], fp)
            fp.close()
      else:
        # print('it doenst exist!')
        # print(compiledLocalPath + file)
        if not os.path.exists(compiledLocalPath):
          os.makedirs(compiledLocalPath)
        with open(compiledLocalPath + file, 'w+') as fp:
          json.dump(modJson, fp)
          fp.close()
  
  
  
    

def rollup_mods(mod_files_list: list[Mod]):
  clean_working_dir()

  for mod in mod_files_list:
    process_mod_file_structure(mod.pathName, mod.files_touched)

