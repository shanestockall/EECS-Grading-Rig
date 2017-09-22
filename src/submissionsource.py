from abc import ABCMeta, abstractmethod, abstractproperty
import datetime
import requests
import hashlib
import hmac
import base64
import json

#Get the current time, printed in the right format
def nowAsStr():
  currentTime = datetime.datetime.utcnow()
  prettyTime = currentTime.strftime('%a, %d %b %Y %H:%M:%S GMT')
  return prettyTime

# Default Student Class
class Student: 
	__metaclass__ = ABCMeta

	def __init__(self):
		self.name = None 
		self.student_id = None
		self.email = None
		self.assignment_grade = None
		self.final_grade = None

# Canvas Student Class
class CanvasStudent(Student):
	def __init__(self):
		self.canvas_id = None


# Default Submission Class
class Submission: 
	__metaclass__ = ABCMeta


# Default Canvas Implementation for the Submission Class
class CanvasSubmission(Submission):
	def __init__(self):
		self.student = None # see class Student
		self.timestamp = None # submission timestamp
		self.zip_path = None # path to zip file (from Canvas)
		self.unzipped_path = None # path to unzipped folder
		self.log_path = None # path to log file
		self.late = None # bool
		self.score = None # score 
		self.final_grade = None # score, including any late penalties

	

class SubmissionSource:

	# GetSubmissions(Assignment) => List(Submission)
	# Downloads a set of submissions from a CMS, returns a list of submissions

	@abstractmethod
	def GetSubmissions():
		pass


class CanvasSubmissionSource(SubmissionSource):

	# Currently entirely taken from https://stackoverflow.com/questions/42656247/how-can-i-use-canvas-data-rest-api-using-python
	# Stack overflow user - fernandojsp
	# This is just a placeholder until I get my own API key and can actually write something to interact with the API 
	
	def GetSubmissions():
		#Set up the request pieces
		apiKey = 'your_key'
		apiSecret = 'your_secret'
		method = 'GET'
		host = 'api.inshosteddata.com'
		path = '/api/account/self/dump'
		timestamp = nowAsStr()

		requestParts = [
		  method,
		  host,
		  '', #content Type Header
		  '', #content MD5 Header
		  path,
		  '', #alpha-sorted Query Params
		  timestamp,
		  apiSecret
		]

		#Build the request
		requestMessage = '\n'.join(requestParts)
		print (requestMessage.__repr__())
		hmacObject = hmac.new(apiSecret, '', hashlib.sha256)
		hmacObject.update(requestMessage)
		hmac_digest = hmacObject.digest()
		sig = base64.b64encode(hmac_digest)
		headerDict = {
		  'Authorization' : 'HMACAuth ' + apiKey + ':' + sig,
		  'Date' : timestamp
		}

		#Submit the request/get a response
		uri = "https://"+host+path
		print (uri)
		print (headerDict)
		response = requests.request(method='GET', url=uri, headers=headerDict, stream=True)

		#Check to make sure the request was ok
		if(response.status_code != 200):
		  print ('Request response went bad. Got back a ', response.status_code, ' code, meaning the request was ', response.reason)
		else:
		  #Use the downloaded data
		  jsonData = response.json()
		  print json.dumps(jsonData, indent=4)






	


