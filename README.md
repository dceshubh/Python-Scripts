# Python-Scripts
It contains all scripts related to automated downloading of favourite shows both from kickass and Youtube.

Dependencies:
1) beautifulSoup
2) tabulate

To make this script a CRON Job do the following :
a) type crontab -e in the terminal
b) add the following statement as per your needs:
ex: 00 11,20 * * * DISPLAY=:0 gnome-terminal -e /home/dceshubh/Downloads/Download-Scripts/daily_shows_download.py
