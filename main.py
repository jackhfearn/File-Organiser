#!/usr/bin/env python

"""
FILE ORGANISER AND MANIPULATOR
A program to explore file-processing in Python.
Also an excuse to try out replit.com and sync to Github

To-Do:
- Method to collect absolute and relative file locations
- Directory tree map in console?
- Output to csv of all file data
- Rename file command
- Move file command
- Duplicate file command (and save to same/different directory)
- Clone file/directory command

# https://docs.python.org/3/library/stat.html
# https://docs.python.org/3/library/os.html#module-os
"""

import os
from datetime import datetime


def index_files(directory):
	"""Searches through a directory and records data on each file. 
	If a sub-directory is found, the function recursively calls itself"""
	
	directory_list = []
	for file in directory:
		if os.path.isdir(file):  # Is a directory/folder
			timestamp = datetime.utcfromtimestamp(file.stat().st_mtime)
			size = file.stat().st_size
			directory_list.append((file.name, file.path, timestamp.strftime('%d %b %Y'), size))
			
			temp_list = index_files(os.scandir(file))
			for item in temp_list:
				directory_list.append(item)
		else:  # Is a file
			timestamp = datetime.utcfromtimestamp(file.stat().st_mtime)
			size = file.stat().st_size
			directory_list.append((file.name, file.path, timestamp.strftime('%d %b %Y'), size))
			
	return directory_list


def output_file_list(indexed_list):
	"""Formats the file data for console output"""
	for item, path, date, size in indexed_list:
		print(item, " - Last accessed: ", date, " - ", str(size) + "B", " - ", path)


def main():
	with open('Demo2.txt', 'w') as f:
		data = 'some data to be written to the file'
		f.write(data)

	my_path = 'Folder 1'
	print(os.listdir(my_path))
	directory = os.scandir(my_path)
	output = index_files(directory)
	output_file_list(output)


if __name__ == "__main__":
	main()
