#!/bin/python3


from changedir import cd
import sys
import string
import errno, os
from pathchecks import is_pathname_valid, isValidFilename 
from cmakelistshelpers import *

def argumentsValid(arg1 : str, arg2 : str) -> bool:
    if (os.path.isdir(arg1) and isValidFilename(arg2) and is_pathname_valid(arg1 + arg2)):
        return True
    elif (os.path.isdir(arg2) and isValidFilename(arg1) and is_pathname_valid(arg2 + arg1)):
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("bad argument count : needs  two arguments")
    if not argumentsValid(sys.argv[1], sys.argv[2]) :
        sys.exit("invalid arguments : must give a valid path and a valid library name")
    if os.path.isdir(sys.argv[1]) :
        path = sys.argv[1]
        libname = sys.argv[2]
    else:
        path = sys.argv[2]
        libname = sys.argv[1]
    try:
        with cd(path): # Going into root src directory
            os.mkdir(libname) # Creating a directory for the library
            with cd(libname):
                srcdirname = "src"
                testdirname = "test"
                cml = "CMakeLists.txt"
                # Create library's root CMakeLists.txt file, and filling it
                with open(cml,'w') as rootcmakelistsfile:
                    writelibraryrootcmakelistsfile(rootcmakelistsfile, srcdirname, testdirname)    
                # Create source and test directories
                os.mkdir(srcdirname)
                os.mkdir(testdirname)
                with cd(srcdirname):
                    with open(cml, 'w') as libcmakelistsfile:
                       writesrcdircmakelistsfile(libcmakelistsfile, libname) 
                with cd(testdirname):
                    with open(cml, 'w') as testcmakelistsfile:
                        writetestcmakelistsfile_gtest(testcmakelistsfile, libname, testdirname)
    except PermissionError as pe:
        sys.exit("Permission denied")
    except FileNotFoundError as fnfe:
        sys.exit("Directory not found")
    except FileExistsError as fee:
        sys.exit("Directory with this library name already exists")
    except Exception as e:
        sys.exit("Failed")
    print("Done")    

