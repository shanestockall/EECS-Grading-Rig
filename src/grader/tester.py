import csv
import json
import zipfile 
import os
import subprocess
from shutil import copy
import re
import math
from shutil import move
import unzipper

##############################################
################## GLOBALS ###################
##############################################

global csFiles                  #["UndirectedGraph.cs", "BinaryHeap.cs"],          # Directory to copy CS files from, relative to unzipped project directory
global templatePath             #"./template/PathPlanner/",           			        # Directory to copy CS files to, relative to root directory
global slnPath                  #"\"./template/PathPlanner.sln\"",         			# Location of sln file relative to root
global dllPath           	# Location of test dll relative to root
global msBuild
global msTest

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

def get_immediate_subdirectories(d):
    return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])

def grade(params):
  load_config()
  grades = {}
  if params['modeSingle']:
    for root, dirs, files in os.walk("./unzipped"):
      for fname in files:
        print "\n\n========================\nGrading: " + fname + "\n========================"
        copy(os.path.join(root, fname), params['templatePath'])
        os.remove(params['templatePath'] + params['csFiles'][0])
        os.rename(params['templatePath'] + fname, params['templatePath'] + params['csFiles'][0])

        print "\n\nBuilding...\n"
        results = buildAndTest(params['slnPath'], params['dllPath'], fname)
        grades[fname] = results
        print "Results: \n" 
        print results
  else:
    for proj in get_immediate_subdirectories("./unzipped"):
      if not "__MACOSX" in proj:
        print "\n\n========================\nGrading: " + proj + "\n========================"
        missing = False
        listFound = False
        for codeFile in params['csFiles']:
          found = False
          for root, dirs, files in os.walk(proj):
            for fname in files:
              if fname.lower().endswith(codeFile.lower()) and not "._" in fname:
                print("Copying: " + fname)
                copy(os.path.join(root, fname), params['templatePath'])
                try:
                  os.rename(params['templatePath'] + fname, params['templatePath'] + codeFile)
                except:
                  pass
                found = True

              if params['defaultFile'] and fname == params['defaultFileName']:
                print "Copying custom listDict"
                copy(os.path.join(root, fname), params['templatePath'])
                listFound = True

          if not found:
            missing = True

        if params['defaultFile'] and  not listFound:
          print "Using template listDict"
          copy(params['defaultFileName'], params['templatePath'])

        if not missing:
          print "\n\nBuilding...\n"
          results = buildAndTest(params['slnPath'], params['dllPath'], proj[11:])
          grades[proj[11:]] = results
          print "Results: \n" 
          print results
        else:
          print "MISSING FILES"
          exportTests("MISSING FILES",proj[11:])
          grades[proj[11:]] = {'passed': 0, 'failed': 89}
  return grades



