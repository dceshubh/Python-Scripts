import urllib.request, json, os, sys
from bs4 import BeautifulSoup

def get_playlist_name(url):
	try:
		print ("Fetching HTML of url: ", url)
		request = urllib.request.urlopen(url)
		a = request.read()
		print ("Got HTML")
		decoded_string = a.decode('utf-8')
		soup = BeautifulSoup(decoded_string,"lxml")
		links=soup.find('h1',attrs={"class":"pl-header-title"})
		c=links.string
		c = c.replace("\n","")
		c = c.lstrip()
		return c

	except:
		print("An error occured during parsing the website")
		return "playlist"


f = open('download.txt','r')
lines = f.readlines()
updates = lines
original_location = os.getcwd()

for a in lines:
	command = "youtube-dl "+ a
	curr_location = os.getcwd()
	if 'playlist' in a:
		print("playlist Detected")
		folder_name = get_playlist_name(a)
		print(folder_name)
		folder_name = str(folder_name)
		curr_location = os.getcwd()
		location = curr_location+ "/" + folder_name
		if not os.path.isdir(location):
			print("Creating New Folder",folder_name)
			os.mkdir(location)
		print("Changing Directory !! Moving to :",location)
		os.chdir(location)
		print("Directory Changed Successfully !! Inside the Directory : ",location)
	try:
		print("downloading",a)
		x = os.system(command)
		if x==0:
			print("download complete")
			updates.remove(a)
	except:
		print("Downloading could not be completed because of an error raised by Youtube-dl")
	finally:
		os.chdir(curr_location)
	print(updates)

f.close()

os.chdir(original_location)
f = open('download.txt','w')
for a in updates:
	f.write(a)
f.close()	