from abc import ABCMeta, abstractmethod, abstractproperty
import time
import re 
import math
import os

class Gradebook: 
	__metaclass__ = ABCMeta

	@abstractmethod
	def RegisterGrade(sub):
		pass

	@abstractmethod
	def EndOfGradingSession(sub):
		pass

	def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

class CanvasGradebook:

	global assignmentName # name of assignment (email subject line, gradebook)
	global writeFile # file to contain grade results by ID (CSV)

	def RegisterGrade(sub):
		#upload to canvas via API

	# TO DO: Don't do all at once, do by submissions
	def EndOfGradingSession(sub):
		parse_results()

	def parse_results():
		wFile = open(writeFile, 'w+')
        wFile.write("ID, " + assignmentName + "\n")

        #path of results directory
        resultsDir = os.listdir("../results/")

        #regex to search for student ids
        REGEX = '[0-9]{1,2}\/[0-9]{1,2}'

        #for each file in the results dir, find a student ID, get the grade, and print them to a file
        for file in resultsDir:
                f = open('./results/' + file)
                for line in f: 
                        if re.match(REGEX, line):
                                student = re.search('_[0-9]{4,5}_',file)
                                numerator,denominator = re.match(REGEX,line).group(0).split("/")
                                grade = math.ceil(100*float(numerator)/float(denominator))

                                wFile.write(student.group(0).replace("_", "") + "," + str(grade))


