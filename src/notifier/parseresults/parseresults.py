import re
import math
import os

##############################################
################## GLOBALS ###################
##############################################

global writeFile
global assignmentName

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

                
def main():
        load_config()
        wFile = open(writeFile, 'w+')
        wFile.write("ID, " + assignmentName + "\n")

        #path of results directory
        resultsDir = os.listdir("./results/")

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

if __name__ == '__main__':
    main()
