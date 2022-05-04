import shutil
import useScriptCompareFunctions
import json
import os
import fnmatch

def get_json(path):
  with open(path) as fp:
    jsonDump = json.load(fp)
    fp.close() # force file stream closed, not sure its necessary but /shrug
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
  for path in modJSONPaths:
    for file in modJSONPaths[path]:
      compiledLocalPath = localPathRoute + path + '/'
      compiledModPath = modPathRoute + mod  + path + '/'
      if file == 'mod_info.json':
        merge_mod_info(compiledModPath + file)
        continue
      modJson = get_json(compiledModPath + file)
      if os.path.exists(compiledLocalPath + file):
        # print('it exists!')
        existingJSON = get_json(compiledLocalPath + file)
        mergedJSON = useScriptCompareFunctions.compareDicts(existingJSON, modJson)
        if mergedJSON['level'] != 3:
          with open(compiledLocalPath + file, 'w') as fp:
            json.dump(mergedJSON['json'], fp)
            fp.close()
      else:
        # print('it doenst exist!')
        if not os.path.exists(compiledLocalPath):
          os.makedirs(compiledLocalPath)
        with open(compiledLocalPath + file, 'w+') as fp:
          json.dump(modJson, fp)
          fp.close()
    

def get_touched_JSONs_from_mods(enabled):
  mods = {}
  for dirName, subdirList, fileList in os.walk('../../'):
    jsonFiles = fnmatch.filter(fileList, '*.json')
    if len(jsonFiles) > 0:
      modName = dirName.split('/')[2]
      for mod in enabled:
        if mod == modName:
          modifiedDir = '/' + dirName[(7+len(modName)):len(dirName)]
          if modName not in mods:
            mods[modName] = {}
          mods[modName][modifiedDir] = jsonFiles
  return mods

def rollup_mods(mod_files_list):
  clean_working_dir()

  for mod in mod_files_list:
    process_mod_file_structure(mod, mod_files_list[mod])

modsTouchedFiles = get_touched_JSONs_from_mods(['CrusoeThreads', 'CrusoeYamSeng', 'Old Conduits'])

rollup_mods(modsTouchedFiles)
