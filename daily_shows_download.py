#!/usr/bin/python3
import os
import sys

def main():
    path_name = os.path.dirname(sys.argv[0])
    option1 = None
    option2 = None
    option3 = None
    full_path = os.path.abspath(path_name)
    os.chdir(full_path)
    print(" ************************ START ******************* ")
    print(" -------------- RUNNING SCRIPTS -----------")
    print(" -------------- Running YOUTUBE Shows Script ----------------")
    try:
        option1 = sys.argv[1]
    except:
        print(" No Argument Specified !! Using Default ")
    command = "./download_youtube.py option1"
    x = os.system(command)
    if x==0:
        print(" -------- Youtube Shows Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" -------------- Running Torrent Shows Script ----------------")
    try:
        option2 = sys.argv[2]
    except:
        print(" No Argument Specified !! Using Default ")
    command = "./download_torrent.py option2"
    x = os.system(command)
    if x==0:
        print(" -------- Torrent Shows Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" -------------- Running YOUTUBE Videos Download Script ----------------")
    try:
        option3 = sys.argv[3]
    except:
        print(" No Argument Specified !! Using Default ")
    command = "./download_script.py option3"
    x = os.system(command)
    if x==0:
        print(" -------- Youtube Videos Download Script Completed -------- ")
    else:
        print(" -------- Interrupted By User ----------- ")

    print(" ************************ END ************************** ")
    print(option1, option2, option3)


if __name__ =='__main__':
    main()
