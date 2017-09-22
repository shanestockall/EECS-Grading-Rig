import time
import submissionsource as ss
import submissionunpacker as su
import builder as b
import tester as t
import reporter as r
import gradebook as g
import csv
import subprocess


def main():
        # ss.GetSubmissions()
        unpacker = su.CanvasSubmissionUnpacker()
        unpacker.Unpack("../assignments/")
        submissions = unpacker.submissions
        builder = b.CSharpBuilder()
        tester = t.CSharpTester()
        reporter = r.DefaultReporter()
        grader = g.CanvasGradebook()
        for submission in submissions:
                # runs tests and exports to "../results" directory
                builder.Build(submission)
                tester.Test(submission)
        # using the ../results directory, sends transcripts to students
        reporter.send_transcripts()
        # right now, this outputs a .csv file to upload to Canvas
        grader.parse_results()
        # runs moss
        subprocess.call(['../moss/runmoss.sh'])
                
	

if __name__ == '__main__':
	main()
