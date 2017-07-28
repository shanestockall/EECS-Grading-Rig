from abc import ABCMeta, abstractmethod, abstractproperty
import time
import csv
import smtplib
import pandas
import glob
import re
from email.mime.text import MIMEText

class Reporter: 
	__metaclass__ = ABCMeta

	@abstractmethod
	def SendReport(sub):
		pass

	def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

class DefaultReporter:
	global instructorEmail # email login
	global instructorPassword # email password
	global className # name of class (used in email subject line)
	global assignmentName # name of assignment (email subject line, gradebook)
	global listofEmails # Csv file of student (Email, Canvas_ID)

	# TO DO - don't do everything at once, optimize!
	def SendReport(sub):
		send_transcripts()


	def send_transcripts():
		emailList = []

		# gather list of emails, ids from external csv files
		data = pandas.read_csv(listofEmails)
		emails = list(data.Email)
		ids = list(data.Canvas_ID)
		print ids

		#find all result files
		listfiles = glob.glob("./results/*.txt")

		#Time to start SMTP!
		s = smtplib.SMTP('smtp.gmail.com', 587)     
        s.ehlo()
        s.starttls()
        s.login(instructorEmail, instructorPassword)

        # For each assignment log file
        for file in listfiles:

        	try: 
        		email = ""
        		# Read in a log file
                fp = open(file, 'rb')
                msg = MIMEText(fp.read())
                fp.close()

                # Extract studentID
                studentID = re.search("_[0-9]{4,5}_", str(file))
                studentID = studentID.group(0).strip("_")
                print studentID

                # Find email associated with studentID
                # Can't use ids.index(studentID) because ids doesn't hold strings
                for student in ids:
                        index = ids.index(student)
                        if str(student) == studentID:
                                email = emails[index]
                                print email
                
                msg['Subject'] = className + " " + assignmentName + " Transcript"
                msg['From'] = instructorEmail
                msg['To'] = email

                # Send the message

                s.sendmail(instructorEmail, [email], msg.as_string())

                print "Sent transcript to: " + email 

            except:
            	# in the case that Gmail's SMTP times us out
            	# (this will happen a lot, given the phishing attempts recently)
            	# sleep for 5 minutes (Google will chill after that)
            	# append the file to the end of the files list (so we don't miss it!)

            	time.sleep(300)
            	listfiles.append(file)
            	continue



