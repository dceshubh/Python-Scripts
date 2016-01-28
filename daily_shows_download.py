#!/usr/bin/python3
import os
import sys


def main():
    path_name = os.path.dirname(sys.argv[0])
    full_path = os.path.abspath(path_name)
    os.chdir(full_path)
    print(" ************************ START ******************* ")
    print(" -------------- RUNNING SCRIPTS -----------")
    print(" -------------- Running YOUTUBE Shows Script ----------------")
    command = "./download_youtube.py"
    x = os.system(command)
    if x == 0:
        print(" -------- Youtube Shows Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" -------------- Running Torrent Shows Script ----------------")
    command = "./download_torrent.py"
    x = os.system(command)
    if x == 0:
        print(" -------- Torrent Shows Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" -------------- Running YOUTUBE Videos Download Script ----------------")
    command = "./download_script.py"
    x = os.system(command)
    if x == 0:
        print(" -------- Youtube Videos Download Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" ************************ END ************************** ")


if __name__ == '__main__':
    main()
