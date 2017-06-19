import csv
import smtplib
import pandas
import glob
import re
from email.mime.text import MIMEText


##############################################
################## GLOBALS ###################
##############################################

global instructorEmail
global instructorPassword
global className
global assignmentName
global listofEmails

##############################################

def load_config():
    with open('config.json') as cfg:
        config = json.load(cfg)
        for key in config.keys():
            if key in globals():
                globals()[key] = config[key]

def main():
        load_config()
        emailList = []

        data = pandas.read_csv(listofEmails)
        emails = list(data.Email)
        ids = list(data.Canvas_ID)
        print ids


        listfiles = glob.glob("./results/*.txt")
        #print listfiles

        # Oh boy! Let's talk SMTP!
        s = smtplib.SMTP('smtp.gmail.com', 587)     
        s.ehlo()
        s.starttls()
        s.login(instructorEmail, instructorPassword)

        # For each assignment log file
        for file in listfiles:
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

                print "sent transcript to" + email 

        s.quit()

if __name__ == '__main__':
        main()
