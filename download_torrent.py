#!/usr/bin/python3

# -*- coding: utf-8 -*-
# Author: pantuts
# Modified by : dceshubh
# URL: http://pantuts.com
# Agreement: You can use, modify, or redistribute this tool under the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.
# Dependencies:
# requests: https://pypi.python.org/pypi/requests
# beautifulSoup4: https://pypi.python.org/pypi/beautifulsoup4/4.3.2
# tabulate: https://pypi.python.org/pypi/tabulate

from bs4 import BeautifulSoup
import os
import re
import requests
import subprocess
import sys
import tabulate


class OutColors:
    DEFAULT = '\033[0m'
    BW = '\033[1m'
    LG = '\033[0m\033[32m'
    LR = '\033[0m\033[31m'
    SEEDER = '\033[1m\033[32m'
    LEECHER = '\033[1m\033[31m'


def helper():
    print(OutColors.DEFAULT + "\nSearch torrents from Kat.cr ;)")


def select_torrent():
    torrent = input('>> ')
    return torrent


def download_torrent(url):
    fname = os.getcwd() + '/' + url.split('title=')[-1] + '.torrent'

    try:
        schema = ('https:')
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        r = requests.get(schema + url, headers=headers, stream=True)
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except requests.exceptions.RequestException as e:
        print('\n' + OutColors.LR + str(e))
        sys.exit(1)

    return fname


def updated_value(name):
    show_name = name.split(" ")[-1]
    episode_number = int(show_name.split("e")[-1])
    name = name.replace(str(episode_number), str(episode_number + 1))
    return name


def update_name(name, list_shows):
    for i, show in enumerate(list_shows):
        if show == name:
            list_shows[i] = updated_value(name)
            break


def aksearch(flag, list_shows):
    helper()
    tmp_url = 'https://kat.cr/usearch/'
    if flag is True:
        query = input('Type query: ')
        url = tmp_url + query + '/'

    else:
        url = tmp_url + flag + '/'

    try:
        cont = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit('\n' + OutColors.LR + str(e))

    # check if no torrents found
    if not re.findall(r'Download torrent file', str(cont.content)):
        print('Torrents found: 0')
    else:
        soup = BeautifulSoup(cont.content)

        # to use by age, seeders, and leechers
        # sample:
        # 700.46 MB
        # 5
        # 2 years
        # 1852
        # 130
        al = [s.get_text() for s in soup.find_all('td', {'class':'center'})]

        href = [a.get('href') for a in soup.find_all('a', {'title':'Download torrent file'})]
        size = [t.get_text() for t in soup.find_all('td', {'class':'nobr'}) ]
        title = [ti.get_text() for ti in soup.find_all('a', {'class':'cellMainLink'})]
        age = al[2::5]
        seeders = al[3::5]
        leechers = al[4::5]

        # for table printing
        table = [[OutColors.BW + str(i+1) + OutColors.DEFAULT if (i+1) % 2 == 0 else i+1,
                    OutColors.BW + title[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else title[i],
                    OutColors.BW + size[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else size[i],
                    OutColors.BW + age[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else age[i],
                    OutColors.SEEDER + seeders[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else OutColors.LG + seeders[i] + OutColors.DEFAULT,
                    OutColors.LEECHER + leechers[i] + OutColors.DEFAULT if (i+1) % 2 == 0 else OutColors.LR + leechers[i] + OutColors.DEFAULT] for i in range(len(href))]
        print()
        print(tabulate.tabulate(table, headers=['No', 'Title', 'Size', 'Age', 'Seeders', 'Leechers']))

        # torrent selection
        if len(href) == 1:
            torrent = 1
        else:
            print('\nSelect torrent: [ 1 - ' + str(len(href)) + ' ] or [ M ] to go back to main menu or [ Q ] to quit')
            torrent = select_torrent()
            if torrent == 'Q' or torrent == 'q':
                sys.exit(0)
            elif torrent == 'M' or torrent == 'm':
                aksearch(flag, list_shows)
            else:
                if int(torrent) <= 0 or int(torrent) > len(href):
                    print('Use eyeglasses...')
                else:
                    print('Download >> ' + href[int(torrent)-1].split('title=')[-1] + '.torrent')
                    fname = download_torrent(href[int(torrent)-1])
                    subprocess.Popen(['xdg-open', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if flag is not True:
                        update_name(flag, list_shows)


def download_from_file():
    fname = "download_torrent_shows"
    f = open(fname, 'r')
    list_shows = f.readlines()
    f.close()
    print(" ----- Found %s number of torrents in the file ----- " % len(list_shows))
    print(" ----- Name of Torrents are as follows ------ ")
    for i,name in enumerate(list_shows):
        print(" -- %s -- %s -- " % (i + 1, name))
        aksearch(name, list_shows)

    f = open(fname, "w")
    for show in list_shows:
        f.write(show)

    f.close()


def update_file():
    fname = "download_torrent"
    f = open(fname, 'r')
    list_shows = f.readlines()
    f.close()
    print(" ----- Found %s number of torrents in the file ----- " % len(list_shows))
    print(" ----- Name of Torrents are as follows ------ ")
    new_list = list()
    for i,name in enumerate(list_shows):
        print(" -- %s -- %s -- " % (i + 1, name))
        ch = input(" ------ Enter y/Y to keep this entry in the file ------ ")
        if ch is 'y' or ch is 'Y':
            new_list.append(name)

    while True:
        ch = input(" ----- Do you want to add new entries to the file ? ----- ")
        if ch is 'Y' or ch is 'y':
            name = input(" ----- Enter the name ----- ")
            new_list.append(name)
        else:
            break

    f = open(fname, 'w')
    for name in new_list:
        f.write(name)

    f.close()


if __name__ == '__main__':
    query = True
    print(" ------ Enter 1 to search for a particular show ----- ")
    print(" ------ Enter 2 to continue downloading from download_torrent file ------ ")
    print(" ------ Enter 3 to update the download_torrent file ----- ")
    print(" ------ Enter any value greater than 3 to quit ------ ")
    choice = input(" ----- Enter your choice ----- ")
    choice = int(choice)
    if choice is 1:
        try:
            aksearch(query, None)
        except KeyboardInterrupt:
            print(" ----- User Interruption ----- ")
    elif choice is 2:
        try:
            download_from_file()
        except KeyboardInterrupt:
            print(" ----- User Interruption ----- ")
    elif choice is 3:
        try:
            update_file()
        except KeyboardInterrupt:
            print(" ----- User Interruption ----- ")
    else:
        print(" ------ Quitting ------- ")
        sys.exit(0)
