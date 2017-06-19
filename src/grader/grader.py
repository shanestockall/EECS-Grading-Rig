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
import builder
import tester


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

def main():
  load_config()
  unzip("./assignments") 

  params = {
    'modeSingle': False,                                        			# Student uploaded single CS file
    'csFiles': csFiles,          # Directory to copy CS files from, relative to unzipped project directory
    'templatePath': templatePath,           			        # Directory to copy CS files to, relative to root directory
    'slnPath': slnPath,         			# Location of sln file relative to root
    'dllPath': dllPath,           	# Location of test dll relative to root
    'defaultFile': False,                                       			# Optional default file if custom file is not uploaded
    'defaultFileName' : "",                                     			# Name of default file. Plase in root
  }

  grades = grade(params)


if __name__ == '__main__':
  main()
