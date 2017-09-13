from abc import ABCMeta, abstractmethod, abstractproperty
import submissionsource
import zipfile 
import os


class SubmissionUnpacker:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.submissions = []

	@abstractmethod
	def Unpack(path_to_assignments):
		pass


class CanvasSubmissionUnpacker(SubmissionUnpacker):

	# Unpack(Path) => void
	# Unpacks all assignments in the assignments directory 
	# Effect: fills paths into the submission object

	def Unpack(path_to_assignments):
		assDir = path = os.path.abspath(path_to_assignments)
		for dirName, subdirList, fileList in os.walk(path_to_assignments):
			print('Found directory: %s' % dirName)
		    for fname in fileList:
		    	filepath = os.path.join(dirName, fname)
		        if filepath.endswith('.zip'):
		        	print('\tUnzipping: %s' % fname)
		        	sub = CanvasSubmission()
		        	sub.zip_path = filepath
		            path = os.path.abspath("./unzipped/").decode('utf-8').strip()
		            sub.unzipped_path = path
		            self.submissions.append(sub)
		            zip = zipfile.ZipFile(filepath.decode('utf-8').strip())
		            zip.extractall(u"\\\\?\\" + path + "\\"+ fname.replace(".zip","").encode('utf-8').strip())



