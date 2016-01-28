#!/usr/bin/python3
import urllib.request, os
from bs4 import BeautifulSoup
import re
from tabulate import tabulate


def get_links(url):
    print(" ------- Fetching HTML of url: %s ------ " % url)
    request = urllib.request.urlopen(url)
    a = request.read()
    print(" ---------- Got HTML ----------- ")
    decoded_string = a.decode('utf-8')
    soup = BeautifulSoup(decoded_string, "lxml")
    try:
        links_h = soup.findAll('h3', attrs={"class": "yt-lockup-title"})
    except:
        links_h = soup.findAll('h3', attrs={'class': 'yt-lockup-title '})
    links = list()
    for link in links_h:
        links.append(link.find('a'))

    durations = list()
    for link in links_h:
        durations.append(link.find('span'))

    return links,durations


def download_video(url):
    command = "/usr/local/bin/youtube-dl " + url
    curr_location = os.getcwd()
    print(" ------ Changing Directory !! Moving to Downloads Folder ------ ")
    os.chdir('..')
    print(" ------ Directory Changed Successfully !! Inside the Directory : %s ------ " % os.getcwd())
    try:
        print(" ----------------------- downloading %s ---------------------" % url)
        x = os.system(command)
        if x == 0:
            print(" ---------------------------- download complete --------------------------")
    except:
        print(" ----------- Downloading could not be completed because of an error raised by Youtube-dl ---------- ")
    finally:
        os.chdir(curr_location)
    return x


def get_next_episode_show(show, episode_number):
    next_episode = int(re.search(r'[0-9]+', episode_number).group(0)) + 1
    next_episode_number = re.sub(r'[0-9]+', str(next_episode), episode_number)
    show = show.replace(episode_number, next_episode_number)
    return show


def start_function():
    fname = "download_youtube_shows"
    f = open(fname, "r")
    shows = f.readlines()
    f.close()
    new_list_shows = list()
    for show in shows:
        show = show.replace("\n", "")
        print(" ------------ PROCESSING SHOW %s ------------- " % show)
        episode_number = re.search(r'(?s)episode(.*)', show.split("||")[0], re.I).group(0)
        if show.split("||")[-1].startswith("http") is not True:
            base_url = "https://www.youtube.com/results?q="
            query = show
            rest_url = urllib.parse.quote(query)
            url = base_url + rest_url
            links, durations = get_links(url)
            table = list()
            for i, link in enumerate(links):
                new_list = list()
                new_list.append(i+1)
                new_list.append(link.string.lower())
                new_list.append(durations[i].string)
                table.append(new_list)

            print(tabulate(table, headers=["S.NO", "TITLE", "DURATION"], tablefmt="fancy_grid"))
            if len(links) >= 1:
                ans = int(input(" ------- Select any value between 1 and %s (both inclusive) to download the corresponding video or select any value greater than %s if donot want to download any video" % (len(links), len(links))))
                if ans > len(links):
                    print(" ------------- No Video Selected ----------------- ")
                    new_list_shows.append(show)
                else:
                    final_link = links[ans-1]['href']
                    final_link = "https://www.youtube.com" + final_link
                    new_list_shows.append(show + "||" + final_link)
                    val = download_video(final_link)
                    if val is 0:
                        new_list_shows.pop()
                        new_list_shows.append(get_next_episode_show(show, episode_number))

            else:
                print(" ------ No Video Available according to the query ------")
                new_list_shows.append(show)
        else:
            final_link = show.split("||")[-1]
            new_list_shows.append(show)
            val = download_video(final_link)
            if val is 0:
                new_list_shows.pop()
                new_list_shows.append(get_next_episode_show(show.split("||")[0], episode_number))

    f = open(fname, "w")
    for show in new_list_shows:
        f.write(show)

    print(" ----------------- UPDATED LIST -----------------")
    print(new_list_shows)
    f.close()


if __name__ == '__main__':
    start_function()
