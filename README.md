# EECS Grading Rig Architecture Plan
### by Shane Stockall

## Requirements 

General grading __driver program__ to take a collection of submissions, iterate through them running unit tests, collect the output, upload grades to canvas, and deliver the log files from the grader to the students as feedback. 

Support late submissions and extensions.

Integration with MOSS

A separate submission program, run by the students, that runs acceptance tests (file existence, directory structure, and specific regexs in certain files)

Integrates with the Canvas API

Packages cheating reports, sent to the dean - with a templated cover letter & diff checker to generate a report 


## Modules

Currently implemented in Python 2.7.13, but open to refactor for Python 3 if necessary. 

* Download submissions from Canvas (investigate if possible)
* Unit tester (basically done, just needs cleaned / commented / tested with other rigs)
* Output -> CSV (done, just clean and comment)
* Join results.csv with gradebook (done)
* Log emailer (done)
* Cheating detection with MOSS 
* Student submission checker / submitter? 
* Cheating report generator 

## Source Files

* emailmatch.py - SQL style join on CAESAR email information with Canvas student IDs (output used by sendtranscripts.py)
* gradematch.py - SQL style join on grades and student information to prep for upload for Canvas
* parseresults.py - dives through the ./results folder to return each student's grade for the assignment
* sendtranscripts.py - dives through the ./results folder, finds the email associated with that student's ID, and then 
* grader.py - unzips all files in ./assignments, then grades each directory in ./unzipped (originally testrigsearch.py)

__For more detailed implementation details, see the architecture plan in the docs.__

Originally developed on top of https://github.com/nikhilpi/visualstudiograder 

Thanks, Nikhil!