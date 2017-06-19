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
global templatePath             #"./template/PathPlanner/",                         # Directory to copy CS files to, relative to root directory
global slnPath                  #"\"./template/PathPlanner.sln\"",              # Location of sln file relative to root
global dllPath            # Location of test dll relative to root
global msBuild
global msTest

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

def buildAndTest(slnPath, dllPath,name):
  load_config()
  buildPath = msBuild + ' ' + slnPath
  build = subprocess.Popen(buildPath, shell=True, stdout=subprocess.PIPE).stdout.read()
  if not "Build FAILED." in build:
    print "\ntesting...\n"
    ####### FOR NEW VERSIONS OF VS, MAKE SURE YOU CAHNGE THIS
    testPath = msTest + ' /testcontainer:'+ dllPath + ' /detail:errormessage'
    output =  subprocess.Popen(testPath, stdout=subprocess.PIPE, shell=True).stdout.read()
    exportTests(output,name)
    results = cleanResults(output)
  else:
    print "NO BUILD"
    exportTests(build,name)
    results = {'passed': 0, 'failed': 99}
  return results

def cleanResults(results):
  #results = results.split('Summary')[1]
  passed = re.search(r'Passed.+\d+', results)
  failed = re.search(r'Failed.+\d+', results)
  if passed:
    passed = passed.group(0)
    passed =  int(re.search(r'\d+',passed).group(0))
  else:
    passed = 0

  if failed:
    failed = failed.group(0)
    failed =  int(re.search(r'\d+',failed).group(0))
  else:
    failed = 0

  return {'passed': passed, 'failed': failed}

def exportTests(out,name):
  outfile = open('./results/'+name+'.txt', 'w')
  outfile.write(out)
  outfile.close()
