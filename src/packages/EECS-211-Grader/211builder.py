from abc import ABCMeta, abstractmethod, abstractproperty
import csv
import json
import zipfile 
import os
import subprocess
from shutil import copy
import re
import math
from shutil import move
import submissionunpacker
import submissionsource

class Builder:
	__metaclass__ = ABCMeta

	# Build(Submission) => Boolean
	@abstractmethod
	def Build(sub):
		pass

	def load_config():
	    with open('config.json') as cfg:
	        config = json.load(cfg)
	        for key in config.keys():
	            if key in globals():
	                globals()[key] = config[key]

class CPPBuilder(Builder):
	global cppFiles                  #["UndirectedGraph.cpp", "BinaryHeap.cpp"],          # Directory to copy CPP files from, relative to unzipped project directory
	global templatePath              #"./template/PathPlanner/",                         # Directory to copy CPP files to, relative to root directory

	def Build(sub):
		load_config()
		name = sub.student.name
		load_config()
		buildPath = "g++ " + templatePath + cppFiles[0] + " -o " + cppFiles[0][:-4]
  		build = subprocess.Popen(buildPath, shell=True, stdout=subprocess.PIPE).stdout.read()
  		if not "error" in build:
  			return True
  		else:
  			return False

