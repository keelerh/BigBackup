import os

os.system("sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl")
os.system("sudo chmod a+rx /usr/local/bin/youtube-dl")
link = open("link.txt", "w").read()
os.system("youtube-dl -o '%(timestamp)s' " + link)
