# Python-Scripts
It contains all the scripts related to automated downloading of favourite shows both from kickass and Youtube.

Dependencies:
1) beautifulSoup
2) tabulate

To make this script a CRON Job do the following :
a) type crontab -e in the terminal
b) add the following statement as per your needs:

ex: 00 11,20 * * * DISPLAY=:0 gnome-terminal -e /home/dceshubh/Downloads/Download-Scripts/daily_shows_download.py

You can also make the following script daily_shows_download.py to be executable from any where by adding following line to the .bashrc file.
export PATH=$PATH:/home/dceshubh/Downloads/Download-Scripts
here Download-Scripts is the folder where daily_shows_download.py file is present

********************************************** USAGE *********************************************************
python3 daily_shows_downlaod.py -1 y -2 y -3 y
ie python3 <file_name> -1 <option for script 1> -2 <option for script 2> -3 <option for script 3>
Note: option is 'y' or 'Y' if you want to run the corresponding script
      For Torrent Shows Script , we have three options 1, 2, 3 .So either we can specify -2 1 or -2 2 or -2 3
      or -2 y if we want to run torrent shows script or specify -2 n or -2 N if donot want to run the script
****************************************************************************************************************