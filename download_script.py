#!/usr/bin/python3
import urllib.request
import os
import sys

from bs4 import BeautifulSoup


def get_playlist_name(url):
    try:
        print("Fetching HTML of url: ", url)
        request = urllib.request.urlopen(url)
        a = request.read()
        print("Got HTML")
        decoded_string = a.decode('utf-8')
        soup = BeautifulSoup(decoded_string, "lxml")
        links = soup.find('h1', attrs={"class": "pl-header-title"})
        c = links.string
        c = c.replace("\n", "")
        c = c.lstrip()
        return c

    except:
        print("An error occured during parsing the website")
        return "playlist"

if sys.argv[1] is None:
    f = open('download.txt', 'r')
    lines = f.readlines()
    updates = lines
    original_location = os.getcwd()
    print(' ---------------- Script Started ---------------- ')
    print(' ----- Found %s URLS to be downloaded ------ ' %len(lines))

    for i, a in enumerate(lines):
        # command = "youtube-dl -f bestvideo+bestaudio "+ a
        # above is to be used if ffmpeg is installed on the system
        print(' --------- Processing URL No %s -------- ' %i + 1)
        command = "/usr/local/bin/youtube-dl " + a
        curr_location = os.getcwd()
        if 'playlist' in a:
            print("playlist Detected")
            folder_name = get_playlist_name(a)
            print(folder_name)
            folder_name = str(folder_name)
            curr_location = os.getcwd()
            location = curr_location + "/" + folder_name
            if not os.path.isdir(location):
                print("Creating New Folder", folder_name)
                os.mkdir(location)
            print("Changing Directory !! Moving to :", location)
            os.chdir(location)
            print("Directory Changed Successfully !! Inside the Directory : ", location)
        try:
            print("downloading", a)
            x = os.system(command)
            if x == 0:
                print("download complete")
                updates.remove(a)
        except:
            print("Downloading could not be completed because of an error raised by Youtube-dl")
        finally:
            os.chdir(curr_location)

    f.close()

    print( ' ----------------------- Updated URLS ------------------ ')
    print(updates)
    os.chdir(original_location)
    f = open('download.txt', 'w')
    for a in updates:
        f.write(a)
    f.close()

else:
    print(" ------------------------ Script Not Executed --------------------- ")
