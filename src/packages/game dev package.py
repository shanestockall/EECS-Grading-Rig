from abc import ABCMeta, abstractmethod, abstractproperty
import builder
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

class Tester:
	__metaclass__ = ABCMeta

	# Test(Submission) => Boolean
	# Effect: Creates a .txt file in the results directory with test results
	@abstractmethod
	def Test(sub):
		pass

	def load_config():
	    with open('config.json') as cfg:
	        config = json.load(cfg)
	        for key in config.keys():
	            if key in globals():
	                globals()[key] = config[key]


class CSharpTester(Tester):

	global csFiles                  #["UndirectedGraph.cs", "BinaryHeap.cs"],          # Directory to copy CS files from, relative to unzipped project directory
	global templatePath             #"./template/PathPlanner/",                         # Directory to copy CS files to, relative to root directory
	global slnPath                  #"\"./template/PathPlanner.sln\"",              # Location of sln file relative to root
	global dllPath            		# Location of test dll relative to root
	global msBuild
	global msTest

	def Test(sub):
		load_config()
		builds = builder.Build(sub)
		if builds:
			testPath = msTest + ' /testcontainer:'+ dllPath + ' /detail:errormessage'
    		output =  subprocess.Popen(testPath, stdout=subprocess.PIPE, shell=True).stdout.read()
    		ExportTests(output, sub.student.name)
    		return True
  		else:
  			ExportTests("BUILD FAILED", sub.student.name)
  			return False

  	def ExportTests(out, name):
  		outfile = open('./results/'+name+'.txt', 'w')
  		outfile.write(out)
  		outfile.close()
