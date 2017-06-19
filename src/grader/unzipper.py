import csv
import json
import zipfile 
import os
import subprocess
from shutil import copy
import re
import math
from shutil import move

def unzip(assignmentsPath):
  assDir = path = os.path.abspath(assignmentsPath)
  for dirName, subdirList, fileList in os.walk(assignmentsPath):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        filepath = os.path.join(dirName, fname)
        if filepath.endswith('.zip'):
          print('\tUnzipping: %s' % fname)
          zip = zipfile.ZipFile(filepath.decode('utf-8').strip())
          path = os.path.abspath("./unzipped/").decode('utf-8').strip()
          zip.extractall(u"\\\\?\\" + path + "\\"+ fname.replace(".zip","").encode('utf-8').strip())
