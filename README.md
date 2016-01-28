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
