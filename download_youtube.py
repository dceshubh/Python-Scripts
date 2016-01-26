import urllib.request, os
from bs4 import BeautifulSoup
import re


def get_links(url):
    print(" ------- Fetching HTML of url: %s ------ "  %url)
    request = urllib.request.urlopen(url)
    a = request.read()
    print(" ---------- Got HTML ----------- ")
    decoded_string = a.decode('utf-8')
    soup = BeautifulSoup(decoded_string,"lxml")
    try:
        links_h = soup.findAll('h3',attrs={"class":"yt-lockup-title"})
    except:
        links_h = soup.findAll('h3', attrs = {'class':'yt-lockup-title '})
    links = list()
    for link in links_h:
        links.append(link.find('a'))
        
    return links
        
 
def download_video(url):
    command = "youtube-dl " + url
    curr_location = os.getcwd()
    location = curr_location.replace("/Download Scripts", "")
    print(" ------ Changing Directory !! Moving to : %s ------ " %location)
    os.chdir(location)
    print(" ------ Directory Changed Successfully !! Inside the Directory : %s ------ " %location)
    try:
        print(" ----------------------- downloading %s ---------------------" %url)
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
    new_list = list()
    for show in shows:
        print(" ------------ PROCESSING SHOW %s ------------- " % show)
        base_url = "https://www.youtube.com/results?q="
        query = show
        rest_url = urllib.parse.quote(query)
        url = base_url + rest_url
        links = get_links(url)
        final_link = None
        try:
            episode_number = re.search(r'(?s)episode(.*)', query, re.IGNORECASE).group(0)
            for link in links:
                link_details = link.string
                link_details = link_details.lower()
                if episode_number in link_details:
                    final_link = link['href']
                    break

            if final_link is not None:
                final_link = "https://www.youtube.com" + final_link
                val = download_video(final_link)
                if val is not 0:
                    new_list.append(show)
                else:
                    new_list.append(get_next_episode_show(show, episode_number))

        except:
            print(" ------ No Video Available according to the query ------")
            new_list.append(show)

        if final_link is None:
            print(" ------ No Video Available according to the query ------")
            new_list.append(show)

    f = open(fname, "w")
    for show in new_list:
        f.write(show)
        f.write("\n")

    print(" ----------------- UPDATED LIST -----------------")
    print(new_list)
    f.close()


if __name__ == '__main__':
    start_function()
            
        
        
        
    
    
    
    