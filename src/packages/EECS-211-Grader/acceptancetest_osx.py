import hashlib
import shutil
import os
from datetime import datetime

list_of_paths_and_strings = [
["assignment1.cpp", "main()"]
]

def main():
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(sys.argv[0])
	os.chdir(dname)
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
	print "The current time is " + " datetime.today()"
	return datetime.today()

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
						print "Found " + string +  " in file."
					else: 
						print string + "not found in file."
						return False
			file.close()
			return True
		except:
			print 'File does not exist. Please make sure all necessary files are in the correct place.'
			return False

def make_txt_file():
	# writes a text file with each of the hashes for each of the files using MD5
	write_file = open("hash.txt", "w+")
	write_file.write("Write time: " + str(get_current_time()) + '\n')

	for file in os.listdir(os.getcwd()):
		if "." in file:
			f_name, file_hash = get_md5_hash(file)
			write_file.write(f_name + '\n')
			write_file.write(file_hash + '\n')

	write_file.close()	

def zip_dir():
	# zips directory using shutil.make_archive()
	zip_name = "submission"
	directory_name = "./tmp"

	os.mkdir("./tmp")

	for file in os.listdir(os.getcwd()):
		try:
			if ".pdf" in file:
				continue
			elif "acceptancetest" in file:
				continue
			else:
				shutil.copy(file, './tmp/')
		except: 
			continue

	shutil.make_archive(zip_name, 'zip', directory_name)

	shutil.rmtree('./tmp')



if __name__ == '__main__':
	main()