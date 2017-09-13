import time
import submissionsource
import submissionunpacker
import builder
import tester
import reporter
import gradebook
import hashlib
import shutil
from zipfile import zipfile
from datetime import datetime

list_of_paths_and_strings = [
["Interpreter/ChainedHashtable.cs", "string_to_search_for", "string_to_search_for2"],
["Interpreter/Dictionary.cs", "string_to_search_for"],
["Interpreter/OpenAddressedHashtable.cs", "string_to_search_for"],
["Interpreter.sln"]
]

def main():
	if acceptance_test():
		make_txt_file()
		zip_dir()


def get_md5_hash(file):
	# opening file
	file_to_hash = open(file)
	read_file = file_to_hash.read()

	# get hash of file
	md5_hash = hashlib.md5(read_file)
	md5_hash_output = md5_hash.hexdigest()

	# print file name and hash
	print "File Name: %s" % file
	print "MD5 Hash: %r" % md5_hash_output

	# return hash 
	return file, md5_hash_output

def get_current_time():
	return datetime.now().time()

def acceptance_test():
	# for each list of the list of paths and strings
	# make sure that a file with that name exists within the folder 
	for my_list in list_of_paths_and_strings:
		path = my_list[0] 
		list_of_strings = my_list[1:]
		try: 
			with open(path) as file:
				for string in list_of_strings:
					if string in file.read():
						print "Found " + string + "in file."
					else: 
						print string + "not found in file."
						return False
			file.close()
			return True
		except: 
			print 'File does not exist. Please make sure all necessary files are in the correct place.'


			return False

def make_txt_file():
	write_file = open("hash.txt", "w+")
	write_file.write("Write time: " + get_current_time() + '\n')

	for file in os.listdir(os.getcwd()):
		f_name, file_hash = get_md5_hash(file)
		write_file.write(f_name + '\n')
		write_file.write(file_hash + '\n')

	write_file.close()	

def zip_dir():
	zip_name = "submission.zip"
	directory_name = "."

	shutil.make_archive(zip_name, 'zip', directory_name)




if __name__ == '__main__':
	main()