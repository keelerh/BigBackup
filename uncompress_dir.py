"""

Please run the following commands (or your OS's variant of these commands).

You need these things installed.

sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl

sudo apt-get install ffmpeg

sudo apt-get install python-qrtools

"""

import qrcode
import sys
import os
import glob

# Downloads the video
link = open("link.txt", "r").read()
os.system("youtube-dl -o '%(id)s' http://www.youtube.com/watch?v=" + link)
#os.system("youtube-dl http://www.youtube.com/watch?v=" + link)

videoName = "'" + link + ".mp4'"

# Splits the .mp4 video into many .png frames
os.system("ffmpeg -i " + videoName + " -r 1 -s 177x177 -f image2 frame-%07d.png")

# The .tar where things are stored
storage = open("storage.tar", "w+")

# Processes each frame and appends the data to storage.tar
#lastFrameNumber = max(glob.iglob('*.[Mm][Pp]4'), key=os.path.getctime)
#print(lastFrameNumber)
#lastFrameNumber = lastFrameNumber[6:13]
#for frame in range(1, (int(lastFrameNumber) + 1)):
for frame in range(1, 4):
	d = qrcode.Decoder()
	framePath = str(frame) + ".png"
	fullFramePath = "frame-" + framePath.zfill(11)
	d.decode(fullFramePath)
	print(d.result)
	storage = open("storage.tar", "a+")
	storage.write(d.result)
		
	
#	os.remove(fullFramePath)



	


	
