#!/usr/bin/python3
import os
import sys
from optparse import OptionParser

''' ********************************************** USAGE *********************************************************
    python3 daily_shows_downlaod.py -1 y -2 y -3 y
    ie python3 <file_name> -1 <option for script 1> -2 <option for script 2> -3 <option for script 3>
    Note: option is 'y' or 'Y' if you want to run the corresponding script
          For Torrent Shows Script , we have three options 1, 2, 3 .So either we can specify -2 1 or -2 2 or -2 3
          or -2 y if we want to run torrent shows script or specify -2 n or -2 N if donot want to run the script
    **************************************************************************************************************
'''

def main():
    path_name = os.path.dirname(sys.argv[0])
    optparser = OptionParser()
    optparser.add_option('-1', '--youtubeShows', dest='youtubeShows', help = 'option for daily youtube shows', default = 'y')
    optparser.add_option('-2', '--torrentShows', dest='torrentShows', help = 'option for daily torrent shows', default = 'y')
    optparser.add_option('-3', '--youtubeVideos', dest='youtubeVideos', help = 'option for youtube videos', default = 'y')
    (options, args) = optparser.parse_args()
    option1 = options.youtubeShows
    option2 = options.torrentShows
    option3 = options.youtubeVideos

    full_path = os.path.abspath(path_name)
    os.chdir(full_path)
    print(" ************************ START ******************* ")
    print(" -------------- RUNNING SCRIPTS -----------")
    if option1 is not 'y' and option1 is not 'Y':
        print(" -------- Youtube Daily Shows Download Script Not Executed !! ---------- ")
    else:
        print(" -------------- Running YOUTUBE Shows Script ----------------")
        command = "./download_youtube.py"
        x = os.system(command)
        if x==0:
            print(" -------- Youtube Shows Script Completed -------- ")
        else:
            print(" -------- Interrupted By User ----------- ")

    if option2 is 'n' or option2 is 'N':
        print(" -------- Torrent Daily Shows Download Script Not Executed !! ---------- ")
    else:
        print(" -------------- Running Torrent Shows Script ----------------")
        command = "./download_torrent.py " + str(option2)
        x = os.system(command)
        if x==0:
            print(" -------- Torrent Shows Script Completed -------- ")
        else:
            print(" -------- Interrupted By User ----------- ")

    if option3 is not 'y' and option3 is not 'Y':
        print(" -------- Youtube Videos Download Script Not Executed !! ---------- ")
    else:
        print(" -------------- Running YOUTUBE Videos Download Script ----------------")
        command = "./download_script.py"
        x = os.system(command)
        if x==0:
            print(" -------- Youtube Videos Download Script Completed -------- ")
        else:
            print(" -------- Interrupted By User ----------- ")

    print(" ************************ END ************************** ")
    #print(option1, option2, option3)


if __name__ =='__main__':
    main()
