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

class CSharpBuilder(Builder):
	global csFiles                  #["UndirectedGraph.cs", "BinaryHeap.cs"],          # Directory to copy CS files from, relative to unzipped project directory
	global templatePath             #"./template/PathPlanner/",                         # Directory to copy CS files to, relative to root directory
	global slnPath                  #"\"./template/PathPlanner.sln\"",              # Location of sln file relative to root
	global dllPath            # Location of test dll relative to root
	global msBuild
	global msTest

	def Build(sub):
		load_config()
		name = sub.student.name
		load_config()
		buildPath = msBuild + ' ' + slnPath
  		build = subprocess.Popen(buildPath, shell=True, stdout=subprocess.PIPE).stdout.read()
  		if not "Build FAILED." in build:
  			return True
  		else:
  			return False

