#!/usr/bin/env python

"""
FILE ORGANISER AND MANIPULATOR
A program to explore file-processing in Python.
Also, an excuse to try out replit.com and sync to GitHub

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
import csv
import pathlib
import math
import os
from datetime import datetime


# def get_current_directory_list(directory):
#     current_dir = os.scandir(directory)
#     directory_list = []
#     for file in current_dir:
#         if os.path.isdir(file):
#             directory_list.append((file.path, file.name))
#     return directory_list
#
# def get_file_list(directory):
#     current_dir = os.scandir(directory)
#     file_list = []
#     for file in current_dir:
#         if os.path.isdir(file):
#             file_list.append((file.path, file.name))
#             file_list += get_file_list(file.path)
#         if os.path.isfile(file):
#                 timestamp = datetime.fromtimestamp(file.stat().st_mtime)
#                 size = file.stat().st_size
#                 file_list.append((file.path, file.name, pathlib.Path(file).suffix, timestamp.strftime('%d %B %Y, %H:%M'), size))
#     return file_list
#
# def get_subdir_file_list(directory):
#     current_dir = os.scandir(directory)
#     file_list = []
#     for file in current_dir:
#         if os.path.isfile(file):
#             timestamp = datetime.fromtimestamp(file.stat().st_mtime)
#             size = file.stat().st_size
#             file_list.append((file.path, file.name, pathlib.Path(file).suffix, timestamp.strftime('%d %B %Y, %H:%M'), size))
#     return file_list
#
# def get_subdirectories(directory):
#     current_dir = os.scandir(directory)
#     directory_list = []
#     for file in current_dir:
#         if os.path.isdir(file):
#             directory_list.append((file.path, file.name))
#             directory_list += get_subdirectories(file.path)
#     return directory_list


def index_files(directory):
    """Searches through a directory and records data on each file.
	If a subdirectory is found, the function recursively calls itself"""

    directory_list = []
    for file in directory:
        if os.path.isdir(file):  # False for directory/folder
            timestamp = datetime.utcfromtimestamp(file.stat().st_mtime)
            size = file.stat().st_size
            directory_list.append((file.path, file.name, "directory", timestamp.strftime('%d %b %Y'), size))

            temp_list = index_files(os.scandir(file))
            for item in temp_list:
                directory_list.append(item)
        else:  # Is a file
            timestamp = datetime.utcfromtimestamp(file.stat().st_mtime)
            size = file.stat().st_size
            directory_list.append((file.path, file.name, pathlib.Path(file).suffix, timestamp.strftime('%d %b %Y'), size))

    return directory_list

def print_directory_list(indexed_list, top):
    """Formats the file data for console output"""
    def size_conversion(f_bytes):
        """Convert size to larger byte denominations for printing"""
        if f_bytes > 999_999_999_999:
            return math.floor(f_bytes / 1_000_000_000_000), "TB"
        elif f_bytes > 999_999_999:
            return math.floor(f_bytes / 1_000_000_000), "GB"
        elif f_bytes > 999_999:
            return math.floor(f_bytes / 1_000_000), "MB"
        elif f_bytes > 999:
            return math.floor(f_bytes / 1_000), "KB"
        else:
            return f_bytes, "B"

    print(top, '\n>>>>>', len(indexed_list))
    top = top[:top.rfind('\\')]
    for i, value in enumerate(indexed_list):
        if os.path.isdir(value[0]):
            print(value[0].replace(top, '*'))
        else:
            file_path, file_name, file_type, file_mdate, file_size = value
            file_size, unit = size_conversion(file_size)
            print(f'>> {file_path.replace(top, "*")} - Last accessed: {file_mdate} - {file_type} - {file_size}{unit} - {file_name}')

def get_file_tree(directory, files, folders=False, subfolders=False):
    current_dir = os.scandir(directory)
    file_tree = []
    for item in current_dir:
        if item.is_dir() and not os.path.islink(item.path):
            if folders:
                file_tree.append((item.path, item.name))
            if subfolders:
                file_tree += get_file_tree(item.path, files, folders, subfolders)
        if item.is_file() and files:
            timestamp = datetime.fromtimestamp(item.stat().st_mtime)
            size = item.stat().st_size
            file_tree.append((item.path, item.name, pathlib.Path(item).suffix, timestamp.strftime('%d %B %Y, %H:%M'), size))
    return file_tree

def get_user_input():
    def action_choice():
        print('''Create list of:
    dd - Folders in Directory
    df - Files in Directory
    da - All Files and Folders in Directory
    sd - Folders in Directory and Subdirectories
    sf - Files in Directory and Subdirectories
    sa - All files and folders, including subdirectories
    ''')
        while True:
            files = False
            directories = False
            subdirectories = False
            try:
                action = input("Select: ")
                match action:
                    case 'dd':
                        directories = True
                    case 'df':
                        files = True
                    case 'da':
                        files = True
                        directories = True
                    case 'sd':
                        subdirectories = True
                        directories = True
                    case 'sf':
                        subdirectories = True
                        files = True
                    case 'sa':
                        files = True
                        directories = True
                        subdirectories = True
                    case _:
                        print('Invalid choice.')
                        action = None
                if action is not None:
                    return files, directories, subdirectories
            except ValueError:
                print('Invalid choice.')

    def directory_choice():
        while True:
            try:
                fdir = input("Input directory:")
                if os.path.exists(fdir):
                    return fdir
                else:
                    raise OSError
            except ValueError:
                print("Invalid input. Please try again.")
            except OSError:
                print("The directory could not be found.")

    return action_choice(), directory_choice()

def main():
    user_action, user_directory = get_user_input()
    files, folders, subfolders = user_action
    print_directory_list(get_file_tree(user_directory, files, folders, subfolders), user_directory)

    # with open('Demo2.txt', 'w') as f:
    #     data = 'some data to be written to the file'
    #     f.write(data)
    #
    # my_path = '<PATH>'
    # print(os.listdir(my_path))
    # directory = os.scandir(my_path)
    # output = index_files(directory)
    # # print_files(output)

    # try:
    #     with open('testlist.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #         filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)  # quotechar='|',
    #         filewriter.writerow(["Name", "Path", "File Type", "Date", "Size"])
    #         filewriter.writerows(output)
    # except FileNotFoundError:
    #     print("The file was not found.")
    # except IOError:
    #     print("IOError occurred")
    # except OSError:
    #     print("OSError occurred")
    # except UnicodeEncodeError:
    #     print("An error encoding a Unicode character occurred.")

if __name__ == "__main__":
    main()
