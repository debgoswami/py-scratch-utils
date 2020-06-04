
import argparse
import os
import glob
import sys
from datetime import datetime
from pathlib import Path

def filenameToTitleString(filename, file_pattern="%d-%m-%Y", title_pattern="%A, %d %B %Y"):
    #Parse filename, craft a Human readable title to all
    file_date = datetime.strptime(filename, file_pattern)
    title_string = "#+TITLE: "+file_date.strftime(title_pattern)+"\n"
    return title_string


def prependLineToFile(prepend_text, filename):
    try:
        print("Opening file:{}".format(filename))
        with open(filename, 'r+') as tFile:
            lines = tFile.readlines()
            if lines[0].startswith('#+TITLE'):
                print("Found existing title. Replacing\n")
                lines[0]=prepend_text
            else:
                lines.insert(0,prepend_text)
    #         tFile.seek(0,0)
    #         tFile.writelines(lines)
        print("Completed processing file: {}\n\n".format(filename))

        
    except Exception as e:
        print("error processing file: {}".format(filename))
        print(e)
    

def getFilesInDirectory(dirpath, depth, file_pattern):
    os_path = os.path.normpath(dirpath)
    file_list = [file for file in list(Path(dirname).glob('**/*')) if Path(file).is_file() and not file.name.endswith('.org')]
    print("\nFound {} files with name matching pattern in {}\n", [file_list.shape, file_pattern])
    return file_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Add root directory/file that contains journal files", default="~/Dropbox/org/journal/")
    parser.add_argument("-d", "--depth", help="Depth to explore when looking for files to change", default=1)
    parser.add_argument("-f", "--file-pattern", help="Enter any limiting patterns of the filenames in the form E.g. %m-%d-%y.org", default="%d-%m-%Y")
    parser.add_argument("--dry-run", help="This will not actually change the file, but provides console output on changes it would have written")
    parser.parse_args()

    #Print out the options to command line (if verbose)
    print("Searching for files in: {}  with depth -{} \n", [parser.path, parser.depth])
    print("\t file pattern: {} \n", parser.file-pattern)
    if parser.dry-run:
        print("\n----------------------\n THIS IS A DRY RUN. NO FILES WILL BE CHANGED!\n-----------------------------\n")
    else:
        print("\nTHIS IS NOT A DRY RUN - FILES WILL BE CHANGED!\n\n Proceed (y/n)?")
    
    #Get list of files
    file_list = getFilesInDirectory(parser.path, parser.depth, parser.file-pattern)
    
    #For each journal file:
    # - Parse the filename
    # - Create a corresponding Title String
    # - Open the file
    # - Add the Title String to the top of the file
    # - Close the file
    # - Print summary

    for thsFilename in file_list:
        try:
            thisTitle = filenameToTitleString(thisFilename)
            prependLineToFile(thisTitle, thisFilename)
        except:
            print("\nError processing file: {}\n", thisFilename)
            pass
                
    
if __name__ == "__main__":
    main()
