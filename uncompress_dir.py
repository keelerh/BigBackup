"""

Please run the following commands (or your OS's variant of these commands).

You need these things installed.

sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl

sudo apt-get install ffmpeg

sudo apt-get install python-qrtools

"""

from qrtools import QR
import os
import glob
import gnupg

# Downloads the video
link = open("link.txt", "w").read()
os.system("youtube-dl -o '%(id)s' https://www.youtube.com/watch?v=" + link)

# Splits the .mp4 video into many .png frames
os.system("ffmpeg -i " + link + ".mp4 -r 60 -s 1920x1080 -f image2 frame-%07d.png")

# The .tar where things are stored
storage = open("storage.tar.gpg", "w+")

def decryptTar()

# Processes each frame and appends the data to storage.tar
lastFrameNumber = max(glob.iglob('*.[Mm][Pp]4'), key=os.path.getctime)
lastFrameNumber = lastFrameNumber[6:13]
for frame in range(1 to (lastFrameNumber + 1)):
	myQR = QR(filename="frame-"+frame.zfill(7)+".png")
	if myQR.decode():
		with open("storage.tar.gpg", "a") as storage:
			storage.write(myQR.data)
	os.remove("frame-"+frame.zfill(7)+".png")



	


	
