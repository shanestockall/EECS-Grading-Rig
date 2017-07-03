 
SubmissionSource

__GetSubmissions() => List(Submission)__
EFFECT: downloads student submissions to the /submissions folder.
Accesses the Canvas API, returns a list of student submission objects.  

A Submission object is: 
* Student Name
* Student Canvas ID
* Submission Timestamp
* Path to the raw data (e.g. ./submissions/sms935-Assignment1.zip)
* Path to the unzipped submission (e.g. ./unzipped/sms935-Assignment1/*)
* Path to log file (e.g. ./results/sms935-Assignment1.txt)
* Whether or not the submission was late
* Final Score (including late penalties if they apply)


Student information would probably be another object with name(s), ID number(s), email address, etc.
I think unzipper would probably want to be refactored so that it was really two classes, one that was a subclass of SubmissionSource and that was a subclass of SubmissionUnpacker

SubmissionUnpacker
* __Unpack(Submission, Prototype) => void__
	Makes a directory with all the files from prototype plus the appropriate files from Submission
	Fills its path into the Submission object

Builder
__Build(Submission) => Boolean__
* Runs the appropriate compiler magic to compile the contents of the unpacked directory
* Appends results to submission’s log file
* Returns true if it successfully built
Your builder would be a subclass of this, perhaps renamed as something like “DefaultBuilder”.  Or maybe we call the abstract builder class “BuilderBase” or “ABuilder” or whatever, and just call yours “builder’.  Whatever works

Tester
__Test(Submission) => boolean__
* Runs the tests on a successfully built submission
* Appends results to submissions’s log file
* Adds score to Submission
* Returns false if it failed completely
	Might want some more complicated return value than just a number

Your tester class would be a subclass of this; again, we can play with naming conventions.
Reporter
__SendReport(Submission) => void__
* Sends log file for Submission to the user

__EndOfGradingSession() => void__
Gets called when the grader is done processing submissions.  This would be so that the SendReport method for the email version of Reporter could just throw the submission in a list or queue and then EndOfGradingSession could open the SMTP connection and send all the emails at once

Gradebook
__RegisterGrade(Submission) => void__
__EndOfGradingSession() => void__
This would be the thing that generated the final CSV file.  Then when we want to deal with the Canvas API, we can make a different implementation of it that uploads the grade directly to Canvas.
 
I’m not wedded to any of these details, but that’s the level of thing that I think we want to be mapping out right now.
 
There’s probably also a separate Assignment object that specifies something about the assignment, e.g. the name of the appropriate column in the CSV file to place the results in, or a path to the directory that everything  should be in.  Perhaps that should be passed to the constructor of every one of these classes.  So then the overall driver code loops something like (apologies for writing it in pidgin C#):
 
submissionSource = new ParticularClassForSubmissionSource(assignment)
submissionUnpacker = new ParticularClassforSubmissionUnpacker(assignment)
…
 
Foreach (submission in submissionSource.GetSubmissions())
    submissionUnpacker.Unpack(submission, assignment.Prototype)
    if (!builder.Build(submission) || !tester.test(submission))
       // Do whatever we do with a dead submission
   else
        gradebook.RegisterGrade(submission)
        reporter.SendReport(submission)
 
subissionSource.EndOfGradingSession()
…
reporter.EndOfGradingSession()
gradebook.EndOfGradingSession()